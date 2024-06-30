package towerdefense;

import java.util.*;

public class TowerDefenseGame {
    private Map map;
    private Player player;
    private List<Wave> waves;
    private Random random;

    public TowerDefenseGame() {
        this.map = new Map();
        this.player = new Player();
        this.waves = new ArrayList<>();
        this.random = new Random();
    }

    public void placeTower(Tower tower, int x, int y) {
        if (map.isCellEmpty(x, y)) {
            map.placeTower(tower, x, y);
        } else {
            System.out.println("La celda está ocupada!");
        }
    }

    public void startWave() {
        Wave wave = new Wave();
        for (int i = 0; i < 3; i++) {
            wave.addEnemy(new Enemy('E', 10, 5));
        }
        waves.add(wave);
        wave.start();
    }

    public void updateGame() {
        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (enemy.isAlive()) {
                    int x = random.nextInt(5);
                    int y = random.nextInt(5);
                    if (map.isCellEmpty(x, y)) {
                        map.placeEnemy(enemy, x, y);
                    } else {
                        player.decreaseBaseHealth(enemy.getDamage());
                    }
                }
            }
        }

        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (!enemy.isAlive()) {
                    player.increaseScore(10);
                }
            }
        }

        waves.removeIf(wave -> wave.getEnemies().stream().allMatch(enemy -> !enemy.isAlive()));
    }

    public void gameState() {
        System.out.println(map);
        System.out.println("Puntuación: " + player.getScore());
        System.out.println("Vida de la base: " + player.getBaseHealth());
    }

    public static void main(String[] args) {
        TowerDefenseGame game = new TowerDefenseGame();
        System.out.println("Welcome to Tower Defense Game!");

        Scanner scanner = new Scanner(System.in);

        while (game.player.getBaseHealth() > 0) {
            try {
                System.out.println("1. Place Tower\n2. Start Wave\n3. Show Game State\n4. Exit");
                if (!scanner.hasNextInt()) {
                    System.out.println("Invalid input. Please enter a number.");
                    scanner.next();  // Clear the invalid input
                    continue;
                }
                int choice = scanner.nextInt();

                switch (choice) {
                    case 1:
                        System.out.print("Enter tower symbol: ");
                        char symbol = scanner.next().charAt(0);
                        System.out.print("Enter tower damage: ");
                        if (!scanner.hasNextInt()) {
                            System.out.println("Invalid input. Please enter a number.");
                            scanner.next();  // Clear the invalid input
                            continue;
                        }
                        int damage = scanner.nextInt();
                        Tower tower = new Tower(symbol, damage);
                        System.out.print("Enter x position: ");
                        if (!scanner.hasNextInt()) {
                            System.out.println("Invalid input. Please enter a number.");
                            scanner.next();  // Clear the invalid input
                            continue;
                        }
                        int x = scanner.nextInt();
                        System.out.print("Enter y position: ");
                        if (!scanner.hasNextInt()) {
                            System.out.println("Invalid input. Please enter a number.");
                            scanner.next();  // Clear the invalid input
                            continue;
                        }
                        int y = scanner.nextInt();
                        game.placeTower(tower, x, y);
                        break;
                    case 2:
                        game.startWave();
                        game.updateGame();
                        break;
                    case 3:
                        game.gameState();
                        break;
                    case 4:
                        System.exit(0);
                    default:
                        System.out.println("Invalid choice.");
                }

                if (game.player.getBaseHealth() <= 0) {
                    System.out.println("Game Over!");
                }
            } catch (NoSuchElementException e) {
                System.out.println("Input error: " + e.getMessage());
                scanner.nextLine();  // Clear the invalid input
            }
        }

        scanner.close();
    }
}


/*
package towerdefense;

import java.util.*;

public class TowerDefenseGame {
    private Map map;
    private Player player;
    private List<Wave> waves;
    private Random random;

    public TowerDefenseGame() {
        this.map = new Map();
        this.player = new Player();
        this.waves = new ArrayList<>();
        this.random = new Random();
    }

    public void placeTower(Tower tower, int x, int y) {
        if (map.isCellEmpty(x, y)) {
            map.placeTower(tower, x, y);
        } else {
            System.out.println("La celda está ocupada!");
        }
    }

    public void startWave() {
        Wave wave = new Wave();
        for (int i = 0; i < 3; i++) {
            wave.addEnemy(new Enemy('E', 10, 5));
        }
        waves.add(wave);
        wave.start();
    }

    public void updateGame() {
        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (enemy.isAlive()) {
                    int x = random.nextInt(5);
                    int y = random.nextInt(5);
                    if (map.isCellEmpty(x, y)) {
                        map.placeEnemy(enemy, x, y);
                    } else {
                        player.decreaseBaseHealth(enemy.getDamage());
                    }
                }
            }
        }

        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (!enemy.isAlive()) {
                    player.increaseScore(10);
                }
            }
        }

        waves.removeIf(wave -> wave.getEnemies().stream().allMatch(enemy -> !enemy.isAlive()));
    }

    public void gameState() {
        System.out.println(map);
        System.out.println("Puntuación: " + player.getScore());
        System.out.println("Vida de la base: " + player.getBaseHealth());
    }

    public static void main(String[] args) {
        TowerDefenseGame game = new TowerDefenseGame();
        System.out.println("Welcome to Tower Defense Game!");

        Scanner scanner = new Scanner(System.in);

        while (game.player.getBaseHealth() > 0) {
            try {
                System.out.println("1. Place Tower\n2. Start Wave\n3. Show Game State\n4. Exit");
                int choice = scanner.nextInt();

                switch (choice) {
                    case 1:
                        System.out.print("Enter tower symbol: ");
                        char symbol = scanner.next().charAt(0);
                        System.out.print("Enter tower damage: ");
                        int damage = scanner.nextInt();
                        Tower tower = new Tower(symbol, damage);
                        System.out.print("Enter x position: ");
                        int x = scanner.nextInt();
                        System.out.print("Enter y position: ");
                        int y = scanner.nextInt();
                        game.placeTower(tower, x, y);
                        break;
                    case 2:
                        game.startWave();
                        game.updateGame();
                        break;
                    case 3:
                        game.gameState();
                        break;
                    case 4:
                        System.exit(0);
                    default:
                        System.out.println("Invalid choice.");
                }

                if (game.player.getBaseHealth() <= 0) {
                    System.out.println("Game Over!");
                }
            } catch (NoSuchElementException e) {
                System.out.println("Input error: " + e.getMessage());
                scanner.nextLine();  // Clear the invalid input
            }
        }

        scanner.close();
    }
}

package towerdefense;

import java.util.*;

public class TowerDefenseGame {
    private Map map;
    private Player player;
    private List<Wave> waves;
    private Random random;

    public TowerDefenseGame() {
        this.map = new Map();
        this.player = new Player();
        this.waves = new ArrayList<>();
        this.random = new Random();
    }

    public void placeTower(Tower tower, int x, int y) {
        if (map.isCellEmpty(x, y)) {
            map.placeTower(tower, x, y);
        } else {
            System.out.println("La celda está ocupada!");
        }
    }

    public void startWave() {
        Wave wave = new Wave();
        for (int i = 0; i < 3; i++) {
            wave.addEnemy(new Enemy('E', 10, 5));
        }
        waves.add(wave);
        wave.start();
    }

    public void updateGame() {
        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (enemy.isAlive()) {
                    int x = random.nextInt(5);
                    int y = random.nextInt(5);
                    if (map.isCellEmpty(x, y)) {
                        map.placeEnemy(enemy, x, y);
                    } else {
                        player.decreaseBaseHealth(enemy.getDamage());
                    }
                }
            }
        }

        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (!enemy.isAlive()) {
                    player.increaseScore(10);
                }
            }
        }

        waves.removeIf(wave -> wave.getEnemies().stream().allMatch(enemy -> !enemy.isAlive()));
    }

    public void gameState() {
        System.out.println(map);
        System.out.println("Puntuación: " + player.getScore());
        System.out.println("Vida de la base: " + player.getBaseHealth());
    }

    public static void main(String[] args) {
        TowerDefenseGame game = new TowerDefenseGame();
        System.out.println("Welcome to Tower Defense Game!");

        Scanner scanner = new Scanner(System.in);

        while (game.player.getBaseHealth() > 0) {
            System.out.println("1. Place Tower\n2. Start Wave\n3. Show Game State\n4. Exit");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter tower symbol: ");
                    char symbol = scanner.next().charAt(0);
                    System.out.print("Enter tower damage: ");
                    int damage = scanner.nextInt();
                    Tower tower = new Tower(symbol, damage);
                    System.out.print("Enter x position: ");
                    int x = scanner.nextInt();
                    System.out.print("Enter y position: ");
                    int y = scanner.nextInt();
                    game.placeTower(tower, x, y);
                    break;
                case 2:
                    game.startWave();
                    game.updateGame();
                    break;
                case 3:
                    game.gameState();
                    break;
                case 4:
                    System.exit(0);
                default:
                    System.out.println("Invalid choice.");
            }

            if (game.player.getBaseHealth() <= 0) {
                System.out.println("Game Over!");
            }
        }

        scanner.close();
    }
}



package towerdefense;

import java.util.*;

public class TowerDefenseGame {
    private Map map;
    private Player player;
    private List<Wave> waves;
    private Random random;

    public TowerDefenseGame() {
        this.map = new Map();
        this.player = new Player();
        this.waves = new ArrayList<>();
        this.random = new Random();
    }

    public void placeTower(Tower tower, int x, int y) {
        if (map.isCellEmpty(x, y)) {
            map.placeTower(tower, x, y);
        } else {
            System.out.println("La celda está ocupada!");
        }
    }

    public void startWave() {
        Wave wave = new Wave();
        for (int i = 0; i < 3; i++) {
            wave.addEnemy(new Enemy('E', 10, 5));
        }
        waves.add(wave);
        wave.start();
    }

    public void updateGame() {
        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (enemy.isAlive()) {
                    int x = random.nextInt(5);
                    int y = random.nextInt(5);
                    if (map.isCellEmpty(x, y)) {
                        map.placeEnemy(enemy, x, y);
                    } else {
                        player.decreaseBaseHealth(enemy.getDamage());
                    }
                }
            }
        }

        for (Wave wave : waves) {
            for (Enemy enemy : wave.getEnemies()) {
                if (!enemy.isAlive()) {
                    player.increaseScore(10);
                }
            }
        }

        waves.removeIf(wave -> wave.getEnemies().stream().allMatch(enemy -> !enemy.isAlive()));
    }

    public void gameState() {
        System.out.println(map);
        System.out.println("Puntuación: " + player.getScore());
        System.out.println("Vida de la base: " + player.getBaseHealth());
    }

    public static void main(String[] args) {
        TowerDefenseGame game = new TowerDefenseGame();
        System.out.println("Welcome to Tower Defense Game!");

        Scanner scanner = new Scanner(System.in);

        while (game.player.getBaseHealth() > 0) {
            System.out.println("1. Place Tower\n2. Start Wave\n3. Show Game State\n4. Exit");
            int choice = scanner.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter tower symbol: ");
                    char symbol = scanner.next().charAt(0);
                    System.out.print("Enter tower damage: ");
                    int damage = scanner.nextInt();
                    Tower tower = new Tower(symbol, damage);
                    System.out.print("Enter x position: ");
                    int x = scanner.nextInt();
                    System.out.print("Enter y position: ");
                    int y = scanner.nextInt();
                    game.placeTower(tower, x, y);
                    break;
                case 2:
                    game.startWave();
                    game.updateGame();
                    break;
                case 3:
                    game.gameState();
                    break;
                case 4:
                    System.exit(0);
                default:
                    System.out.println("Invalid choice.");
            }

            if (game.player.getBaseHealth() <= 0) {
                System.out.println("Game Over!");
            }
        }

        scanner.close();
    }
}



package towerdefense;

import java.util.*;

public class TowerDefenseGame {
    private Map map;
    private Player player;
    private List<Wave> waves;

    public TowerDefenseGame() {
        this.map = new Map();
        this.player = new Player();
        this.waves = new ArrayList<>();
    }

    public void placeTower(Tower tower, int x, int y) {
        map.placeTower(tower, x, y);
    }

    public void startWave() {
        Wave wave = new Wave();
        waves.add(wave);
        wave.start();
    }

    public void gameState() {
        System.out.println(map);
        System.out.println("Puntuación: " + player.getScore());
        System.out.println("Vida de la base: " + player.getBaseHealth());
    }
    public static void main(String[] args) {
        TowerDefenseGame game = new TowerDefenseGame();
        System.out.println("Welcome to Tower Defense Game!");

    }
}
*/

