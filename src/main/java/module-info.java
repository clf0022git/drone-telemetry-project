module com.droneplayback.droneplayback {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.web;
    requires javafx.media;

    requires org.controlsfx.controls;
    requires eu.hansolo.tilesfx;

    opens com.droneplayback.droneplayback to javafx.fxml;
    exports com.droneplayback.droneplayback;
}