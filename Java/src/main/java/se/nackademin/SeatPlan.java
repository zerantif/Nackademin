package se.nackademin;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.Arrays;
import java.util.Random;


public class SeatPlan implements Serializable {
    static String columnIdentifiers[] = { "A", "B", "C", "D", "E", "F" };
    static int numRows = 9;

    //rows and columns

    Passenger[][] seats = new Passenger[numRows][columnIdentifiers.length];

    static Random rand = new Random(); //random method to generate numbers

    public void getPassengerManifest() {
        System.out.println("Passenger manifest:");
        System.out.println("-----------------------------------------------------------------");
        System.out.println();
        System.out.println("  Seat   Name                         Birth date");
        System.out.println("  ----------------------------------------------");
        for (int row = 0 ; row < numRows ; row++) {
            for (int col = 0 ; col < columnIdentifiers.length ; col++) {
                Passenger p = seats[row][col];
                if ( p != null ) {
                    System.out.printf("  %2s%s    %-20s %12s\n", row+1, columnIdentifiers[col], p.fullName, p.birthDate);
                }
            }
        }
        System.out.println("  ----------------------------------------------");
        System.out.println();
        System.out.printf("Total number of passengers: %s\n", this.countOccupiedSeats());
        System.out.println("-----------------------------------------------------------------");
    }

    //enhanced loop to print the seats plan
    public void getSeatPlan() {    
        System.out.printf("  ");
        for (int col = 0 ; col < columnIdentifiers.length ; col++ ) {
            System.out.printf("%s %s", 
                              (col == columnIdentifiers.length / 2) ? " " : "",
                              columnIdentifiers[col]);
        }
        System.out.println();

        for (int row = 0 ; row < numRows ; row++) {
            System.out.printf("%2s ", row+1);
            for (int col = 0 ; col < columnIdentifiers.length ; col++) {
                System.out.printf("%s%s ", 
                                  (col == columnIdentifiers.length / 2) ? " " : "",
                                  seats[row][col] == null ? "-" : "X");             
            }
            System.out.println();
        }

    }

    private int getRowFromSeat(String seat) {
        return Integer.parseInt(seat.substring(0, 1)) - 1;
    }
    private int getColumnFromSeat(String seat) {
        return Arrays.asList(columnIdentifiers).indexOf(seat.substring(1, 2));  
    }

    private void validateSeatString(String seat) throws IllegalArgumentException {
        //is string two characters long?
        if ( seat.length() != 2 )
            throw new IllegalArgumentException("Seat must be two characters long.");

        //is the first character 1..this.numRows?
        int row = Integer.parseInt(seat.substring(0, 1)) - 1;
        if ( row < 0 || row > numRows - 1 )
            throw new IllegalArgumentException("Incorrect row number.");

        //is the second chacter found in this.columnIdentifiers?
        int col = Arrays.asList(columnIdentifiers).indexOf(seat.substring(1, 2));
        if ( col == -1 )
            throw new IllegalArgumentException("Incorrect column name.");
    }

    //return seat status : true=occupied false=empty
    public boolean isSeatOccupied(String seat) throws IllegalArgumentException {
        this.validateSeatString(seat);
        return seats[this.getRowFromSeat(seat)][this.getColumnFromSeat(seat)] != null;
    }

    public void assignSeat(String seat, Passenger p) throws IllegalArgumentException {
        this.validateSeatString(seat);
        if (isSeatOccupied(seat))
            throw new IllegalArgumentException("Seat already booked.");
        seats[this.getRowFromSeat(seat)][this.getColumnFromSeat(seat)] = p;
    }

    public int getNumberOfSeats() {
        return numRows * columnIdentifiers.length;
    }

    //returns null if plane is fully booked.
    public String getRandomUnoccupiedSeat() {
        int row, column;

        do {
             if (this.countOccupiedSeats() == numRows * columnIdentifiers.length) {
                 //plane is fully booked!
                 return null;
             }
             row = rand.nextInt(numRows); //randomly select row
             column = rand.nextInt(columnIdentifiers.length); //randomly select column
        } while (seats[row][column] != null);

        return String.valueOf(row+1) + columnIdentifiers[column];
    }

    public int countOccupiedSeats() {
        int num_occupied = 0;
        for (int row = 0 ; row < numRows ; row++ )
            for (int col = 0 ; col < columnIdentifiers.length ; col++ )
                num_occupied += seats[row][col] == null ? 0 : 1;
        return num_occupied;
    }

    //don't care if we change anything in our class.
    private static final long serialVersionUID = 1L;

    //handle saving and loading of our internal state.
    private void writeObject(ObjectOutputStream os) throws IOException {
        os.writeObject(seats);
    }

    private void readObject(ObjectInputStream is) throws ClassNotFoundException, IOException {       
        seats = (Passenger[][])is.readObject();
    }

}