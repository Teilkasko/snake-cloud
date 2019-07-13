//import { Observable } from 'rxjs';
//import { tap, map } from 'rxjs/operators';


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

function initRx() {
	console.log("initRx");

    let namespace = '/snake';
    let socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    let updates = rxFromIO(socket, 'updates');
    updates.pipe(
    	rxjs.operators.tap(ev => console.log("UPDATES", ev))
    );
}

document.addEventListener("DOMContentLoaded", function() {
	initRx();
});