



function func1()
{
    function func2()
    {
        function func3()
        {
            //var a = 2;
            function func4()
            {
                console.log(a + 1);
            }
            func4();
        }
        console.log(a+1);
        func3();
    }
    func2();
    //var a = 1;
}

var a = 1;
func1();
