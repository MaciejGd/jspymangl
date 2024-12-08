function new_test(){
    var first_scope;
}
let func_expr = function (){
    var second_scope = 3;
}
var test_obj = {
    "new_one" : function()
    { 
        const third_scope = 2;
    },
    new_func : function(){

    }
}

let zero_index;
//console.log(new_test);