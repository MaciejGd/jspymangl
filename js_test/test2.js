
const variable = {
    x : 5,
    c : [],
    y : "dawaj",
    set current(name){
        this.c.push(name);
    },
    "property" : "newone"
}
const tab = [1,2,3];

for (let i in tab)
{
    console.log(i);
}

variable.current("new name");
variable[x] = 3;
let new_one = 2;
new_one = 12;