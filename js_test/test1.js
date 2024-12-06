const var1 = 12;
const var2 = 23;

function func(param) {
    return ()=>{
        console.log("Func exec with param: " + param);
        for (var i = 0; i <= param; i++)
        {
            console.log(i);
        }
    }
}

let new_func = func(2);
new_func();



