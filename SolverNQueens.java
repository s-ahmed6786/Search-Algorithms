/**
 * File: SolverNQueens.java
 * Author: Syed Mustafa Ahmed
 * Date: October 22, 2023
 * Purpose:
 *      Solve for N Queens with given input array of size N
 * Description:
 *      This project uses iterative repair to solve for N Queens,
 *
 */

package com.company;
import java.util.*;

public final class SolverNQueens {

    static int[] chessboard;
    static int[] d1;
    static int[] d2;
    static boolean debug_statements = true;

    public static void main(String[] args) {
        int size = 25;

        try {
            solveIterativeRepair(size);
            displayChessboard();
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    /**
     * Run x number of trials for n input size and print times/average times
     *
     * @param size Size of input Array
     * @param number_of_trials Number of trials
     * @return Description of the return value.
     *
     */
    private static void runTrials(int size, int number_of_trials){
        System.out.println("Input size: " + size);
        long totalTime = 0;

        for (int i = 1; i <= number_of_trials; i++) {
            long start_time = System.nanoTime(); // empirical analysis

            try {
                solveIterativeRepair(size);
                //displayChessboard();
            } catch (Exception e) {
                e.printStackTrace();
            }

            long end_time = System.nanoTime();
            long elapsedTime = end_time - start_time;
            totalTime += elapsedTime; // Accumulating the time taken
            System.out.printf("%.8f\n", elapsedTime * 1e-9); // Displaying time to 8 decimal places
        }

        double averageTime = (double) totalTime / number_of_trials; // Calculating the average
        System.out.printf("Average time taken: %.8f Seconds\n", averageTime * 1e-9); // Displaying average time to 8 decimal places
    }

    /**
     * Solves N Queens using Iterative Repair
     *
     * @param size Size of input Array
     *
     */
    private static void solveIterativeRepair(int size) throws Exception {
        // Throw error if N is not a valid size
        if (size < 4) {
            throw new Exception("Size must be greater than 3 for iterative repair method.");
        }

        int swap_counter = 0;
        int collisions = 0;

        // Debug Counters
        int count = 1;
        int nested_for_count = 0;

        // Fill Chessboard/D1/D2 arrays
        initializeChessboard(size);

        // Best case scenario - permutation is correct
        if (getBoardCollisions() == 0) {
            if (debug_statements) {
                System.out.println("Run " + count + ":");
                System.out.println("Number of Swaps Done: " + swap_counter);
                System.out.println("Number of Collisions: " + collisions);
                System.out.println("Number of times if statement checked: " + nested_for_count);
                System.out.println();
            }
            return;
        }

        do {
            swap_counter = 0;

            // Iterate through every permutation of i,j
            for (int i = 0; i < chessboard.length - 1; i++) {
                for (int j = i + 1; j < chessboard.length; j++) {

                    nested_for_count++;
                    // check queen_i diagonals
                    int iIndexD1 = getD1IndexFromQueenPos(i);
                    int iIndexD2 = getD2IndexFromQueenPos(i);

                    // check queen_j diagonals
                    int jIndexD1 = getD1IndexFromQueenPos(j);
                    int jIndexD2 = getD2IndexFromQueenPos(j);

                    // If queen i or j is under attack
                    if (d1[iIndexD1] > 1 || d2[iIndexD2] > 1 || d1[jIndexD1] > 1 || d2[jIndexD2] > 1) {

                        // Get Old Collisions
                        int old_collisions = getBoardCollisions();

                        // swap i and j
                        swap(i, j);

                        // Get New Collisions
                        int new_collisions = getBoardCollisions();

                        //If swap does not reduce collisions, swap back
                        if (old_collisions <= new_collisions) {
                            swap(i, j);
                        } else {
                            swap_counter++;
                        }
                    }
                }
            }

            // Get Board Collisions
            collisions = getBoardCollisions();

            if (debug_statements) {
                System.out.println("Run " + count + ":");
                System.out.println("Number of Swaps Done: " + swap_counter);
                System.out.println("Number of Collisions: " + collisions);
                System.out.println("Number of times if statement checked: " + nested_for_count);
                System.out.println();
            }

            // If board has been sorted to the best of its ability, and collisions still exist, reset board
            if (swap_counter == 0 && collisions > 0) {
                count++;
                initializeChessboard(size);
                if (debug_statements) {
                    System.out.println("======================");
                }
            }
        }
        // while Solution not found
        while (collisions > 0);
    }

    /**
     * Create chessboard with random values (One queen per row, one queen per column)
     *
     * @param n Size of input Array
     *
     */
    public static void initializeChessboard(int n) {
        // Initialize Chessboard and Diagonal Arrays
        chessboard = new int[n];
        d1 = new int[n * 2 - 1];
        d2 = new int[n * 2 - 1];

        // Create an arraylist to pull values from
        ArrayList<Integer> availableValues = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            availableValues.add(i);
        }

        // Fill chessboard array with random values 0-n
        Random rand = new Random();
        for (int i = 0; i < chessboard.length; i++) {
            int randomIndex = rand.nextInt(availableValues.size());
            chessboard[i] = availableValues.get(randomIndex);
            availableValues.remove(randomIndex);
        }
        initializeDiagonals();
    }


    /**
     * Initialize D1 and D2 from chessboard values
     *
     */
    public static void initializeDiagonals() {
        //Clear D1 and D2 before counting occurrences of queens on diagonals (may not be necessary)
        Arrays.fill(d1, 0);
        Arrays.fill(d2, 0);

        // Count occurrences of queens on positive and negative diagonals
        for (int i = 0; i < chessboard.length; i++) {

            d1[(i + chessboard[i])]++;
            d2[(i - chessboard[i] + chessboard.length - 1)]++;
        }
    }

    /**
     * Display Chessboard into terminal
     *
     */
    public static void displayChessboard() {
        // Nested for loop to print board
        for (int row = 0; row < chessboard.length; row++) {
            for (int col = 0; col < chessboard.length; col++) {
                // print 'Q ' if queen occupies space, '. ' if not
                System.out.print(chessboard[col] == row ? " Q " : " . ");
            }
            System.out.println();
        }
    }

    /**
     * Find positive diagonal index from given chessboard value
     *
     * @param index queen position
     * @return index of D1 for which queen position lies on
     *
     */
    private static int getD1IndexFromQueenPos(int index) {
        return (index + chessboard[index]);
    }

    /**
     * Find negative diagonal index from given chessboard value
     *
     * @param index queen position
     * @return index of D2 for which queen position lies on
     *
     */
    private static int getD2IndexFromQueenPos(int index) {
        return (index - chessboard[index]) + (chessboard.length - 1);
    }

    /**
     * Swap i and j queens and update d1 and d2 accordingly
     *
     * @param queen_i chessboard index of queen i
     * @param queen_j chessboard index of queen j
     *
     */
    private static void swap(int queen_i, int queen_j) {
        int iIndexD1Old = getD1IndexFromQueenPos(queen_i);
        int iIndexD2Old = getD2IndexFromQueenPos(queen_i);
        int jIndexD1Old = getD1IndexFromQueenPos(queen_j);
        int jIndexD2Old = getD2IndexFromQueenPos(queen_j);

        d1[iIndexD1Old]--;
        d2[iIndexD2Old]--;
        d1[jIndexD1Old]--;
        d2[jIndexD2Old]--;

        // Swap Pieces
        int temp = chessboard[queen_i];
        chessboard[queen_i] = chessboard[queen_j];
        chessboard[queen_j] = temp;

        int iIndexD1New = getD1IndexFromQueenPos(queen_i);
        int iIndexD2New = getD2IndexFromQueenPos(queen_i);
        int jIndexD1New = getD1IndexFromQueenPos(queen_j);
        int jIndexD2New = getD2IndexFromQueenPos(queen_j);

        d1[iIndexD1New]++;
        d2[iIndexD2New]++;
        d1[jIndexD1New]++;
        d2[jIndexD2New]++;
    }


    /**
     * Calculate total collisions on board by checking d1 and d2 indices
     *
     */
    private static int getBoardCollisions() {
        int collisions = 0;

        for (int i = 0; i < chessboard.length; i++) {
            int iIndexD1 = getD1IndexFromQueenPos(i);
            int iIndexD2 = getD2IndexFromQueenPos(i);

            if (d1[iIndexD1] > 1) {
                collisions = collisions + d1[iIndexD1] - 1;
            }
            if (d2[iIndexD2] > 1) {
                collisions = collisions + d2[iIndexD2] - 1;
            }
        }
        return collisions;
    }
}

