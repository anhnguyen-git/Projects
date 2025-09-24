// Example JavaScript file with problems

var oldStyleVariable = "Should use let or const";
var anotherVar = 42;

function checkEquality(a, b) {
    console.log("Checking equality"); // Should be removed for production
    
    if (a == b) { // Should use === for strict equality
        console.log("Values are equal");
        return true;
    }
    
    return false;
}

function demonstrateProblems() {
    var counter = 0; // Should use let
    
    for (var i = 0; i < 10; i++) { // Should use let
        console.log("Iteration: " + i);
        counter++;
    }
    
    // Loose equality check
    if (counter == "10") {
        console.log("Counter reached 10");
    }
}

// Call the functions
checkEquality(5, "5");
demonstrateProblems();