document.addEventListener("DOMContentLoaded", function() {

  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }

  /**
   * header class change upon url change event
   */
  const header = document.querySelector("#header");
  const currentPage = window.location.pathname;

    if (currentPage === "/") {
      header.className = "";
      header.classList.add("header--main-page");
    } else if (currentPage === "/add_donation/" || currentPage === "/confirmation/") {
      header.className = "";
      header.classList.add("header--form-page");
    } else {
      header.className = "";
    }


  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation


      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;


      const categoryCheckboxes = document.querySelectorAll('.category');
      const institutions = document.querySelectorAll('.institution');

      categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
          const selectedCategories = Array.from(categoryCheckboxes)
              .filter(checkbox => checkbox.checked)
              .map(checkbox => checkbox.value);

          institutions.forEach(institution => {
            const institutionCategories = institution.dataset.categories;

            if (selectedCategories.every(category => institutionCategories.includes(category))) {
              institution.parentElement.style.display = "flex";
            } else {
              institution.parentElement.style.display = "none";
            }
          });
        });
      });

      const btnNext = document.querySelector("#go_to_summary");
      const bags = document.querySelector(".icon-bag");
      const organization = document.querySelector(".icon-hand");
      const pick_up_address = document.querySelector("#pick_up_address");
      const pick_up_details = document.querySelector("#pick_up_details");


      btnNext.addEventListener('click', function(){
        bags.nextElementSibling.innerText = document.querySelector('[name="bags"]').value;

        institutions.forEach(institution => {
            if (institution.checked) {
                const institutionName = institution.closest('.form-group')
                    .querySelector('.title')
                    .textContent;

                organization.nextElementSibling.innerText = institutionName;
            }
        });

        const address = document.querySelector('[name="address"]').value;
        const city = document.querySelector('[name="city"]').value;
        const postcode = document.querySelector('[name="postcode"]').value;
        const phone = document.querySelector('[name="phone"]').value;

        const addressData = [];
        addressData.push(address, city, postcode, phone);

        const addressLiAll = Array.from(pick_up_address.children);

        addressLiAll.forEach((li, index) => {
          li.innerText = addressData[index];
        });

        const data = document.querySelector('[name="data"]').value;

        const dateObj = new Date(data);
        const day = dateObj.getDate();
        const month = dateObj.getMonth() + 1;
        const year = dateObj.getFullYear();
        const formattedDate = `${day}/${month}/${year}`

        const time = document.querySelector('[name="time"]').value;
        const more_info = document.querySelector('[name="more_info"]').value;

        const detailsData = [];
        detailsData.push(formattedDate, time, more_info);

        const detailsLiAll = Array.from(pick_up_details.children);

        detailsLiAll.forEach((li, index) => {
          li.innerText = detailsData[index];
        });
      });
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();

      const getForm = document.getElementById('donation_add');
      const formData = new FormData(getForm);
      console.log(...formData)

      //fetchinf csrf cookie

      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, "csrftoken".length + 1) === ("csrftoken=")) {
            cookieValue = decodeURIComponent(cookie.substring("csrftoken".length + 1));
            break;
          }
        }
      }

      fetch('http://localhost:8000/confirmation/', {
        headers: {
          "X-CSRFToken": cookieValue
        },
        method: 'POST',
        body: formData,
        credentials: "same-origin"

      })


      // getForm.addEventListener ('submit', function(e){
      // const formData = new FormData(getForm);
      // console.log(formData);
      //     fetch('http://localhost:8000/add_donation/', {
      //     method: 'POST',
      //     body: JSON.stringify(formData)
      //     })
      //     .then(response => response.json())
      //     .then(data => console.log("fromData as quantity" + data))
      //     .catch(error => console.error('Error:', error));
      //     });

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
