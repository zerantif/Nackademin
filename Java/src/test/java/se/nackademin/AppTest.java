package se.nackademin;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.UnsupportedEncodingException;
import java.util.Scanner;

import org.junit.jupiter.api.Test;

public class AppTest {

    @Test
    public void tryLoadAndDump() {
        File f = new File("test_database.dat");
        f.delete();

        App app = new App("test_database.dat");
        app.tryLoadSeatPlanFromFile();
        app.saveSeatPlanToFile();
        f.delete();
    }

    @Test
    public void testMenuExit() throws UnsupportedEncodingException {
        String commandsToSend = "5\n";

        ByteArrayInputStream input = 
            new ByteArrayInputStream(commandsToSend.getBytes("UTF-8"));

        App app = new App("test_database.dat");

        //replace System.in with our "commandsToSend"  
        app.input = new Scanner(input);
        app.processMenu();
    }

    @Test
    public void testMenuRegisterManual() throws UnsupportedEncodingException {
        String commandsToSend = "3\n1A\nFullName\n1971\n5\n";

        ByteArrayInputStream input = 
            new ByteArrayInputStream(commandsToSend.getBytes("UTF-8"));

        new File("test_database.dat").delete();
        App app = new App("test_database.dat");

        //replace System.in with our "commandsToSend"
        app.input = new Scanner(input);

        app.processMenu();
    }
}
