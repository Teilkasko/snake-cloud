function rxFromIO (io, eventName) {
    return rxjs.Observable.create(observer => {
        io.on (eventName, (data) => {
            observer.next(data)
        });
        return {
            dispose : io.close
        }
    });
}

function connectionId (socket) {
	return socket.id.split('#')[1];
}

function connectAsUser (socket, username) {
	console.log("connect as user", username, connectionId(socket));
	socket.emit('command', {'command':'connect', 'username':username});
}

function moveUserSnake(socket, keyEvent) {
    console.log("pressed", keyEvent.key);
    switch (keyEvent.key) {
//        case 'w': socket.emit('command', {'command':'snake_up'}); break;
        case 'a': socket.emit('command', {'command':'snake_left'}); break;
//        case 's': socket.emit('command', {'command':'snake_down'}); break;
        case 'd': socket.emit('command', {'command':'snake_right'}); break;
        default:
    }
}

function showUsersConnected(snakes) {
    const userList = document.getElementById("usersConnected")
    userList.innerText = ""
    snakes.forEach(snake => {
        const user = document.createElement("li")
        user.innerText = snake.username
        userList.appendChild(user)  
    })
}

function drawSnakes(canvas, snakes) {
    width = canvas.width;
    height = canvas.height;
    snakes.forEach(s => {
        var points = [];
        s.points.forEach(p => points.push(new fabric.Point(p[0], p[1])))
        var polyLine = new fabric.Polyline(points, {
            stroke: 'black',
            opacity: 0.25,
            fill: '',
            strokeWidth: 5,
            strokeLineCap: 'round',
            strokeLineJoin: 'round'
        });
        canvas.add(polyLine)
    });
}

function drawPoints(canvas, points) {
    const width = canvas.width;
    const height = canvas.height;
    points.forEach(p => {
        var circle = new fabric.Circle({
            fill: 'red',
            radius: 1,
            left: p[0],
            top: p[1]
        });
        canvas.add(circle)
    });
}

function initRx(canvas) {
	console.log("initRx");

    const namespace = '/snake';
    const socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    const issues = rxFromIO(socket, 'issues');
    issues.subscribe(event => {
        if(event.message == "reload") {
	        location.reload();
	    }
	    if(event.message == "shutdown") {
            alert("The server is shutting down, please reload the page to connect to a new one")
	    }
    })
    const updates = rxFromIO(socket, 'updates');
	updates.subscribe(event => {
		console.log("UPDATES", event);
		canvas.getObjects().forEach(o => {
		    canvas.remove(o);
		});
		const ctx = canvas.getContext('2d');
		ctx.clearRect(0, 0, ctx.width, ctx.height);
	    drawSnakes(canvas, event.snakes);
		drawPoints(canvas, event.points);
		showUsersConnected(event.snakes);
	});

    const connectForm = document.getElementById("connectForm");
    const connect = rxjs.fromEvent(connectForm, 'submit');
    connect.subscribe(event => {
		const username = document.getElementById("username").value;
		connectAsUser(socket, username);
    });

    const ups = rxjs.fromEvent(document, 'keydown').pipe(rxjs.operators.debounceTime(1));
    ups.subscribe(event => {
        console.log("KeyPressed", event);
        moveUserSnake(socket, event);
    });

}

// (0,0) is upper left corner, positive axis right and down
function initArena() {
	console.log("initArena!");
	var canvas = new fabric.StaticCanvas('arena', {
		width: 400,
		height: 400
	});

/*	var points = [];
	var random = fabric.util.getRandomInt;

	points.push(new fabric.Point(100,100));
	points.push(new fabric.Point(200,200));
	points.push(new fabric.Point(250,150));

	console.log("POINTS", points)
	var polyLine = new fabric.Polyline(points, {
		stroke: 'black',
		opacity: 0.25,
		fill: '',
		strokeWidth: 5,
		strokeLineCap: 'round',
		strokeLineJoin: 'round'
	});
	canvas.add(polyLine)
*/
	return canvas;
}

document.addEventListener("DOMContentLoaded", function() {
	var canvas = initArena();
	initRx(canvas);
});