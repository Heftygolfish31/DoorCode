// Door Code Python

import java.io.IOException;
import java.util.concurrent.TimeUnit;
import java.util.Arrays;
import java.util.Scanner;

public class Doorcode {
    // Version constant
    static final String VERSION = "0.1";

    // System constants
    static final String OS = System.getProperty("os.name");

    // Location globals
    static public String location = "";
    static public String locationHumanName = "";

    // Input Controls
    static final public Scanner userInput = new Scanner(System.in);

    // COLOURS
    // ANSI codes used to format terminal text
    class Colour {
        static final public String END = "\033[0m";
        static final public String BOLD = "\033[1m";
        static final public String UNDERLINE = "\033[4m";
        static final public String RED = "\033[31m";
        static final public String GREEN = "\033[32m";
        static final public String YELLOW = "\033[33m";
        static final public String CYAN = "\033[36m";
    }

    // WELCOME
    // Welcome the user on startup
    public static void welcome() {
        // The startup message identifying the program
        String firstLine = Colour.UNDERLINE+"*"+Colour.END+" "+Colour.BOLD+Colour.CYAN+"Java Doorcode v"+VERSION+Colour.END+" "+Colour.UNDERLINE+"*"+Colour.END;
        System.out.println(firstLine);
        // Should a location be used?
        if (locationHumanName != "") {
            String secondLine = "| "+Colour.CYAN+"Location: "+Colour.GREEN+locationHumanName+Colour.END;
            System.out.println(secondLine);
        }
    }

    // CLEAR
    // Clear the screen; start afresh
    public static void clear(Boolean toWelcome) {
        System.out.print("\033[H\033[2J");
        System.out.flush();
        // If the flag is set, the welcome message leads everything
        if (toWelcome) {
            welcome();
        }
    }
    // CLEAR Default Mode
    public static void clear() {
        clear(true);
    }

    // COUNTDOWN
    // Simulate a single-line animation to show a clock timeout, in seconds
    public static void countdown(String action, int count) {
        try {
            // Loop for the number of times to sleep by
            while (count > 0) {
                // Second or seconds?
                String sInSeconds = "s";
                if (count == 1) {
                    sInSeconds = "";
                }
                // Print the warning
                System.out.print(Colour.RED+action+" in "+Colour.BOLD+count+Colour.END+Colour.RED+" second"+sInSeconds+"..."+Colour.END+"\r");
                TimeUnit.SECONDS.sleep(1);
                count--;
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    // COUNTDOWN Default
    public static void countdown(String action) {
        countdown(action, 5);
    }

    // KILLER
    // Kill the program and check first
    public static void killer() {
        // try (userInput) {
            // Prompt the user
            System.out.print(Colour.BOLD+Colour.RED+"Kill the program? [Y/n]: "+Colour.END);
            // Are you sure?
            String checkRaw = userInput.nextLine();
            String check = checkRaw.toLowerCase();
            // Yes, I'm sure
            if (Arrays.asList("", "y", "yes").contains(check)) {
                clear(false);
                System.out.println(Colour.GREEN+"Goodbye!"+Colour.END);
                // Kill the program
                System.exit(0);
            // Neither yes nor no
            } else if (!Arrays.asList("n", "no").contains(check)) {
                System.out.println(Colour.RED+"Input not recognised."+Colour.END);
                // Try again
                killer();
            }
            // No, continue the program
        // }
    }


    public static void main(String[] args) {
        try (userInput) {
            clear();
            killer();
        }

    }
}