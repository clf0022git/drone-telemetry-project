package com.droneplayback.droneplayback.gauges;

import java.io.Serializable;

import com.droneplayback.droneplayback.fields.Field;
import eu.hansolo.tilesfx.Tile;
import eu.hansolo.tilesfx.TileBuilder;
import javafx.beans.value.ChangeListener;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.media.MediaPlayer;
import javafx.stage.Stage;
import javafx.stage.StageStyle;

public abstract class Gauge implements Serializable {
    public transient MediaPlayer mediaPlayer;

    public enum GaugeType {
        CIRCLE90,
        CIRCLE180,
        CIRCLE270,
        CIRCLE360,
        BAR,
        XPLOT,
        XYPLOT,
        CHARACTER,
        TEXT,
        CLOCK,
        TIMESTAMP,
        ONOFF
    };

    public GaugeType gaugeType;
    public transient Tile tile;

    public Gauge() {
        this.mediaPlayer = null;
        int TILE_SIZE = 200;
        this.tile = TileBuilder.create()
            .skinType(Tile.SkinType.CUSTOM)
            .prefSize(TILE_SIZE, TILE_SIZE)
            .maxSize(TILE_SIZE, TILE_SIZE)
            .minSize(TILE_SIZE, TILE_SIZE)
            .title("Gauge")
            .build();
    }

    // Subclasses should implement these methods
    public abstract Field getField();
    public abstract void update();

    public void setTitle(String title) { tile.setTitle(title); }

    public void show() {
        Stage stage = new Stage();
        Pane pane = new Pane();
        Scene scene = new Scene(pane);

        // Set as utility pane for minimal window decorations
        // Default gauge has no title
        stage.initStyle(StageStyle.UTILITY);
        stage.setTitle("");

        // Listens for changes in the stage size and updates the tile size accordingly
        ChangeListener<Number> stageSizeListener = (observable, oldValue, newValue) -> {
            pane.setPrefSize(stage.getWidth(), stage.getHeight());
            tile.setPrefSize(stage.getWidth(), stage.getHeight());
        };

        stage.widthProperty().addListener(stageSizeListener);
        stage.heightProperty().addListener(stageSizeListener);

        stage.show();
    }
}
