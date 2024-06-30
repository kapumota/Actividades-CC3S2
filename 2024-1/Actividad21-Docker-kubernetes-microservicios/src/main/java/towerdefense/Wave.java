/*
package towerdefense;

public class Wave {
    public void start() {
        System.out.println("Oleada iniciada!");
    }
}
*/
package towerdefense;

import java.util.ArrayList;
import java.util.List;

public class Wave {
    private List<Enemy> enemies;

    public Wave() {
        enemies = new ArrayList<>();
    }

    public void addEnemy(Enemy enemy) {
        enemies.add(enemy);
    }

    public List<Enemy> getEnemies() {
        return enemies;
    }

    public void start() {
        System.out.println("Oleada iniciada!");
    }
}
