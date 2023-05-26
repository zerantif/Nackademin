package se.nackademin;

import java.io.Serializable;

public class Passenger implements Serializable {
    public String fullName;
    public String birthDate;

    public Passenger(String fullName, String birthDate) {
        this.fullName = fullName;
        this.birthDate = birthDate;
    }

    public String toString() {
        return "Passenger<'"+fullName+"','"+birthDate+"'>";
    }
}
