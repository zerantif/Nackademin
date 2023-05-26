package se.nackademin;

import java.io.File;
import java.util.Random;
import java.util.Scanner;

public final class App {

    SeatPlan seats; //create object from SeatPlan.java

    String databaseFileName;

    Random random = new Random();

    private static int TICKET_MIN_PRICE = 1000;
    private static int TICKET_MAX_PRICE = 10000;

    protected Scanner input = new Scanner(System.in); //scanner method to scan user inputs

    public App(String databaseFileName) {
        this.databaseFileName = databaseFileName;
    }

    public void processMenu() {
        seats = tryLoadSeatPlanFromFile();

        while(true) {
            getMenu(); 
            int option = input.nextInt();
            input.nextLine(); //this is to make Scanner catch end-of-line after number.
            System.out.println();

            //switch case for options
            switch(option) {

                //get seat plan
                case 1:
                    seats.getSeatPlan();

                    System.out.println();
                    System.out.println("Rows 1-3 are First Class seats.\n"
                    + "Rows 4-9 are Economic Cabin.");

                    break;

                //randomly allocate a seat
                case 2:
                    String freeSeat = seats.getRandomUnoccupiedSeat();
                    if ( freeSeat == null ) {
                        System.out.println("Sorry, due to our fantastic marketing, this flight is fully booked!");
                    } else {
                        //read passenger details here.
                        Passenger passenger = getPassengerInfo();
                        try {
                            seats.assignSeat(freeSeat, passenger);
                            System.out.printf("You were assigned seat %s.\n", freeSeat);
                            int ticketPrice = random.nextInt(TICKET_MAX_PRICE) + TICKET_MIN_PRICE;
                            System.out.printf("You ticket price is ¥ %s.\n", ticketPrice);
                        } catch(IllegalArgumentException e) {
                            throw new AssertionError("Unexpected exception raised. (Should not happen)", e);
                        }
                    }
                    break;
              
                //manually select seat
                case 3:
                    //ask the user for an input
                    System.out.print("Please choose your seat (XX - 1A-9F): ");
                    String chosen_seat = input.nextLine();

                    try {
                        if ( seats.isSeatOccupied(chosen_seat) ) {
                            System.out.println("That seat is currently taken.");
                        } else {
                            System.out.printf("You are booking seat %s.\n", chosen_seat);
                            //read passenger details here.
                            Passenger passenger = getPassengerInfo();
                            seats.assignSeat(chosen_seat, passenger);
                            System.out.printf("You have booked seat %s\n", chosen_seat);
                            int ticketPrice = random.nextInt(TICKET_MAX_PRICE) + TICKET_MIN_PRICE;
                            System.out.printf("You ticket price is %s.\n", ticketPrice);
                        }
                    } catch(IllegalArgumentException e ) {
                        System.out.printf("Incorrect input (%s). Try again.\n", e.getMessage());
                    }
                    break;

                //print passenger manifest
                case 4:
                    seats.getPassengerManifest();
                    break;

                //save and quit
                case 5:
                    saveSeatPlanToFile();
                    System.out.println("Data saved, Bye bye.");
                    return;

                //invalid
                default:
                    System.out.println("Incorrect menu choice!");
                    break;
            }
        }

    }

    //menu method
    void getMenu() {
        System.out.println();
        System.out.print("#### Flight Seat Booking ####\n"
            + "1 - Get seat plan.\n"
            + "2 - Randomly allocate seat.\n"
            + "3 - Select seat manually.\n"
            + "4 - Show passenger manifest.\n"
            + "5 - Quit & save.\n"
            + "Enter option: ");
    }


    private Passenger getPassengerInfo() {
        System.out.printf("Passenger full name: ");
        String fullName = input.nextLine();
        System.out.printf("Passenger birth date: ");
        String birthDate = input.nextLine();

        Passenger passenger = new Passenger(fullName, birthDate);

        return passenger;
    }

    protected SeatPlan tryLoadSeatPlanFromFile() {
        try { 
            seats = (SeatPlan)FilePersistence.readFromFile(new File(this.databaseFileName));
        } catch( Exception e ) {
            System.out.println("Could not load data. ("+e.getMessage()+")");
            System.out.println("Starting with empty flight.");
            seats = new SeatPlan();
        }
        return seats;
    }

    protected void saveSeatPlanToFile() {
        try {
            FilePersistence.writeToFile(new File(this.databaseFileName), seats);
        } catch( Exception e ) {
            System.out.println("ERROR: Failed to save passenger state. ("+e+")");
        }
    }


}