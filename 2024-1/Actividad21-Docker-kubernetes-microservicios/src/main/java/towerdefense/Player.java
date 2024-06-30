package towerdefense;

public class Player {
    private int score;
    private int baseHealth;

    public Player() {
        this.score = 0;
        this.baseHealth = 100;
    }

    public int getScore() {
        return score;
    }

    public void increaseScore(int points) {
        score += points;
    }

    public int getBaseHealth() {
        return baseHealth;
    }

    public void decreaseBaseHealth(int damage) {
        baseHealth -= damage;
    }
}



/*
package towerdefense;

public class Player {
    private int score;
    private int baseHealth;

    public Player() {
        this.score = 0;
        this.baseHealth = 100;
    }

    public int getScore() {
        return score;
    }

    public int getBaseHealth() {
        return baseHealth;
    }
}
*/
