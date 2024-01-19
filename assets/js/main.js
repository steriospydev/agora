const paymentCells = document.getElementsByClassName('date-toggler');
const paymentCellsArray = Array.from(paymentCells); // Convert HTMLCollection to an array

let toggle = true;

function toggleClasses() {
    paymentCellsArray.forEach((paymentCell) => {
    if (toggle) {
        paymentCell.classList.add("text-light");
      paymentCell.classList.remove("text-danger");
    } else {
      paymentCell.classList.add("text-danger");
      paymentCell.classList.remove("text-light");
    }
  });
  toggle = !toggle; // Toggle the flag
}

// Call toggleClasses every second (1000 milliseconds)
setInterval(toggleClasses, 500);


