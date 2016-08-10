var nodeColors = [
    '#2C3E50', // Slate
    '#E74C3C', // Watermelon
    '#3498DB', // Sky Blue
    '#2980B9'  // Ocean Blue
];

var textColor = '#ECF0F1'; // Ice White

var colorSwitch = true;

function makeCanvasFullScreen() {
    var canvas = document.getElementById("demoCanvas");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

function makeNode(page, color, textColor) {
    var title = page['title']
    function handleClick(event) {
        window.open(page['url'], '_blank');
    }

    var circle = new createjs.Shape();
    var text = new createjs.Text(page['title'], '20px Arial');

    circle.graphics.beginFill(color).drawCircle(0, 0, 60);
    text.color = textColor;
    text.x = -30;
    text.y = -10;

    var container = new createjs.Container();
    container.addChild(circle, text);
    container.addEventListener("click", handleClick);

    return container;
}

function dfsDisplay(stage, pages, nodeColors, textColor) {
    var xPos = 150;
    var yPos = window.innerHeight / 2;
    var colorIdx = 0;
    var pageIdx = 0;

    function addNodes() {
        if (pageIdx < pages.length) {
            var node = makeNode(pages[pageIdx], nodeColors[colorIdx], textColor);
            node.x = xPos;
            node.y = yPos;
            stage.addChild(node);
            stage.update();

            xPos += 180;
            pageIdx += 1;
            colorIdx += 1;
            if (colorIdx >= nodeColors.length)
            colorIdx = 0;
        }
    }

    createjs.Ticker.interval = 500;
    createjs.Ticker.addEventListener("tick", addNodes);
}

function bfsDisplay(stage, pages, nodeColors, textColor) {
    var xPos = window.innerWidth / 2;
    var yPos = window.innerHeight / 2;
    var colorIdx = 0;
    var pageIdx = 0;
    var childIdx = 0;
    var children = pages['visited'].length;
    var angleOffset = (2 * Math.PI) / children;

    function addNodes() {
        if (pageIdx == 0) {
            var node = makeNode(pages['visited'][pageIdx], nodeColors[colorIdx], textColor);
            node.x = xPos;
            node.y = yPos;
            stage.addChild(node);
            stage.update();

            pageIdx += 1;
            colorIdx += 1;
            if (colorIdx >= nodeColors.length)
            colorIdx = 0;

        } else if (pageIdx < pages['visited'].length) {
            var node = makeNode(pages['visited'][pageIdx], nodeColors[colorIdx], textColor);
            calcPolarToCartesianCoords(node, xPos, yPos, 250, angleOffset * childIdx);
            stage.addChild(node);
            stage.update();

            pageIdx += 1;
            childIdx += 1;
            colorIdx += 1;
            if (colorIdx >= nodeColors.length)
            colorIdx = 0;
        }
    }

    createjs.Ticker.interval = 500;
    createjs.Ticker.addEventListener("tick", addNodes);
}

function calcPolarToCartesianCoords(node, xPos, yPos, distance, angle) {
    node.x = xPos + (distance * Math.cos(angle));
    node.y = yPos + (distance * Math.sin(angle));
}

function init() {
    makeCanvasFullScreen();

    var stage = new createjs.Stage("demoCanvas");
    bfsDisplay(stage, rawData, nodeColors, textColor);

}

init();
