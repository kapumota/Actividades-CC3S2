import static org.assertj.core.api.Assertions.assertThat;
import org.junit.jupiter.api.Test;
public class FootballTeamTest {
    @Test
    void constructorShouldSetGamesWon() {
        FootballTeam team = new FootballTeam(3);
        //assertThat(team.getGamesWon()).isEqualTo(3);
        assertThat(team.getGamesWon())
                .as("number of games won")
                .isEqualTo(3);
    }
}
/*
public class FootballTeamTest {
    private static final int THREE_GAMES_WON = 3;
    @Test
    void constructorShouldSetGamesWon() {
        FootballTeam team = new FootballTeam(THREE_GAMES_WON);
        assertThat(team.getGamesWon())
            .as("number of games won")
            .isEqualTo(THREE_GAMES_WON);
       }
}
 */