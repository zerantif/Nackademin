package se.nackademin;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class SeatPlanTest {
    private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    private final ByteArrayOutputStream errContent = new ByteArrayOutputStream();
    private final PrintStream originalOut = System.out;
    private final PrintStream originalErr = System.err;

    @BeforeEach
    public void setUpStreams() {
        System.setOut(new PrintStream(outContent));
        System.setErr(new PrintStream(errContent));
    }

    @AfterEach
    public void restoreStreams() {
        System.setOut(originalOut);
        System.setErr(originalErr);
    }

    @Test
    public void shouldNotCrash() {
        new SeatPlan();
    }

    @Test
    public void fullyOccupiedPlane() {
        SeatPlan p = new SeatPlan();
        assertTrue(p.countOccupiedSeats() == 0);
        for( int i = 0 ; i < p.getNumberOfSeats() ; i++ ) {
            String seat = p.getRandomUnoccupiedSeat();
            assertTrue(seat != null);
            p.assignSeat(seat, new Passenger("Tester", "123"));
        }
        //last seat has already been taken - getRandom... should return null
        assertTrue(p.getRandomUnoccupiedSeat() == null);
        assertTrue(p.countOccupiedSeats() == p.getNumberOfSeats());
    }

    @Test
    public void seatPlanPrintout() {
        SeatPlan p = new SeatPlan();
        p.getSeatPlan();

        //empty plane seat plan must not contain 'X'.
        assertFalse(outContent.toString().contains("X"));

        p.assignSeat("1A", new Passenger("Tester", "123"));
        p.getSeatPlan();
        assertTrue(outContent.toString().contains("X"));
    }

    @Test
    public void passengerManifest() {
        SeatPlan p = new SeatPlan();
        assertTrue(p.countOccupiedSeats() == 0);
        p.assignSeat("2A", new Passenger("TesterA", "1971-01-02"));
        p.getPassengerManifest();
        assertTrue(outContent.toString().contains("TesterA"));
        assertTrue(outContent.toString().contains("1971-01-02"));
    }

}
