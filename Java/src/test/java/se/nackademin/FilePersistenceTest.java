package se.nackademin;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import org.junit.jupiter.api.Test;

public class FilePersistenceTest {

    @Test
    public void tryReadingMissingShouldFail() {
        assertThrows(IOException.class, () -> {
            FilePersistence.readFromFile(new File("test_no-such-file.dat"));
        });
    }

    @Test
    public void tryReadingCorruptShouldFail() throws IOException {
        File corruptFile = new File("test_corrupt.dat");
        BufferedWriter writer = new BufferedWriter(new FileWriter(corruptFile));
        writer.write("thisisnotjavaserialized");
        writer.close();
        assertThrows(IOException.class, () -> {
            FilePersistence.readFromFile(corruptFile);
        });
        corruptFile.delete();
    }

    @Test
    public void writeAndReadbackSeatPlan() throws IOException, ClassNotFoundException {
        File seatPlanFile = new File("test_seatplan.dat");

        SeatPlan s = new SeatPlan();
        s.assignSeat("1A", new Passenger("TesterFile", "9876"));
        FilePersistence.writeToFile(seatPlanFile, s);

        s = null;

        s = (SeatPlan)FilePersistence.readFromFile(seatPlanFile);

        assertTrue(s.isSeatOccupied("1A"));

        seatPlanFile.delete();
    }

}
