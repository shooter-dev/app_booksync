import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: window
    width: 640
    height: 480
    visible: true
    title: qsTr("booksync — streaming")

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        RowLayout {
            Layout.fillWidth: true
            spacing: 8

            Button {
                text: controller.running ? qsTr("Stop") : qsTr("Start")
                onClicked: controller.running ? controller.stop() : controller.start()
            }

            Label {
                Layout.fillWidth: true
                text: controller.running ? qsTr("Streaming…") : qsTr("Idle")
                color: controller.running ? "#2a9d8f" : "#888"
            }
        }

        Frame {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                id: list
                anchors.fill: parent
                clip: true
                model: controller.model
                spacing: 4

                delegate: Row {
                    spacing: 8
                    Label {
                        text: "#" + chunkId
                        color: "#888"
                        font.family: "monospace"
                    }
                    Label {
                        text: content
                        wrapMode: Text.WordWrap
                    }
                }

                onCountChanged: positionViewAtEnd()
            }
        }
    }
}
