// console.log('sup')
// var newDiv = $("#message").clone();
// var ul = document.querySelector('ul');
// ul.appendChild(newDiv);
// newDiv.show();

function function1() {
    var newDiv = $("#message").clone();
    newDiv.attr("id","whatever").appendTo('ul') 
    newDiv.show()
}

function1()