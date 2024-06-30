package towerdefense;

public class Tower {
    private char symbol;
    private int damage;

    public Tower(char symbol, int damage) {
        this.symbol = symbol;
        this.damage = damage;
    }

    public char getSymbol() {
        return symbol;
    }

    public int getDamage() {
        return damage;
    }
}

/*
package towerdefense;

public class Tower {
    private char symbol;

    public Tower(char symbol) {
        this.symbol = symbol;
    }

    public char getSymbol() {
        return symbol;
    }
}
*/
