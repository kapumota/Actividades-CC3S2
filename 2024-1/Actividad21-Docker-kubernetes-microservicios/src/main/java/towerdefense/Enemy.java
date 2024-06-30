package towerdefense;

public class Enemy {
    private char symbol;
    private int health;
    private int damage;

    public Enemy(char symbol, int health, int damage) {
        this.symbol = symbol;
        this.health = health;
        this.damage = damage;
    }

    public char getSymbol() {
        return symbol;
    }

    public int getHealth() {
        return health;
    }

    public void takeDamage(int damage) {
        health -= damage;
    }

    public boolean isAlive() {
        return health > 0;
    }

    public int getDamage() {
        return damage;
    }
}
