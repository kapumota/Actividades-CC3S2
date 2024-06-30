package towerdefense;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import static org.mockito.Mockito.*;

public class TowerDefenseGameTest {
    @Mock
    private Map mockMap;

    @Mock
    private Player mockPlayer;

    @InjectMocks
    private TowerDefenseGame game;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    public void testPlaceTower() {
        Tower mockTower = mock(Tower.class);
        when(mockMap.isCellEmpty(2, 2)).thenReturn(true);
        game.placeTower(mockTower, 2, 2);
        verify(mockMap).placeTower(mockTower, 2, 2);
    }
}

