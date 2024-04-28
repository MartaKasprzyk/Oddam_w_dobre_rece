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
   * header class change upon url change event (MK)
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

    // get form input fields (MK)
    getFormInputs() {
      const categoryCheckboxes = document.querySelectorAll('.category');
      const bagsInput = document.querySelector('[name="bags"]');
      const institutions = document.querySelectorAll('.institution');
      const address = document.querySelector('[name="address"]');
      const city = document.querySelector('[name="city"]');
      const postcode = document.querySelector('[name="postcode"]');
      const phone = document.querySelector('[name="phone"]');
      const date = document.querySelector('[name="data"]');
      const time = document.querySelector('[name="time"]');

      return {categoryCheckboxes, bagsInput, institutions, address, city, postcode, phone, date, time};
    }


    // form validation (MK)
    validateForm() {
      const formInputs = this.getFormInputs();

      // get next-step buttons (MK)
      const btnNextStep = document.querySelectorAll('.btn.next-step');

      // disable all next-step buttons (MK)
      btnNextStep.forEach(button => {
        button.disabled = true;
      });

      // validate if category checkbox is checked (MK)
      formInputs.categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
          const anyCheckboxChecked = Array.from(formInputs.categoryCheckboxes).some(checkbox => checkbox.checked);
          btnNextStep[0].disabled = !anyCheckboxChecked;
        });
      });

      const helpBlock = document.createElement('span');
      helpBlock.className = 'help-block';
      helpBlock.style.display = 'none';
      helpBlock.style.fontSize = '18px';
      helpBlock.style.color = 'red';
      helpBlock.id = 'error-message';

      // validate bags input (MK)
      let helpBags = helpBlock.cloneNode(true)
      formInputs.bagsInput.addEventListener('input', function () {
        if (this.value.trim() !== '' && parseInt(this.value.trim()) > 0) {
          btnNextStep[1].disabled = false;
          helpBags.remove();
        } else {
          if (formInputs.bagsInput.parentElement.nextElementSibling === null) {
            formInputs.bagsInput.parentElement.insertAdjacentElement('afterend', helpBags);
          }
          btnNextStep[1].disabled = true;
          helpBags.textContent = 'Ilość worków musi być większa od 0.';
          helpBags.style.display = 'block';
        }
      });


      // validate if institution is chosen (MK)
      formInputs.institutions.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
          if (checkbox.checked) {
            btnNextStep[2].disabled = false;
          }
        });
      });


      // validate address input (MK)
      let helpAddress = helpBlock.cloneNode(true)
      const alphanumericAddress = /^(?=.*[a-zA-Z])(?=.*[0-9])/;
      formInputs.address.addEventListener('input', function () {
        if (formInputs.address.value.trim() !== '' && alphanumericAddress.test(formInputs.address.value.trim())) {
          helpAddress.remove();
        } else {
          if (formInputs.address.parentElement.nextElementSibling === null) {
            formInputs.address.parentElement.insertAdjacentElement('afterend', helpAddress);
          }
          btnNextStep[3].disabled = true;
          helpAddress.textContent = 'Podaj nazwę ulicy i numer domu.';
          helpAddress.style.display = 'block';
        }
      });

      // validate city input (MK)
      let helpCity = helpBlock.cloneNode(true)
      formInputs.city.addEventListener('input', function () {

        if (formInputs.city.value.trim() !== '') {
          helpCity.remove();
        } else {
          if (formInputs.city.parentElement.nextElementSibling === null) {
            formInputs.city.parentElement.insertAdjacentElement('afterend', helpCity);
          }
          btnNextStep[3].disabled = true;
          helpCity.textContent = 'Podaj miasto.';
          helpCity.style.display = 'block';
        }
      });

      // validate postcode input (MK)
      let helpCode = helpBlock.cloneNode(true)
      const postCodePattern = /^\d{2}-\d{3}$/;
      formInputs.postcode.addEventListener('input', function () {


        if (formInputs.postcode.value.trim() !== '' && postCodePattern.test(formInputs.postcode.value.trim())) {
          helpCode.remove();
        } else {
          if (formInputs.postcode.parentElement.nextElementSibling === null) {
            formInputs.postcode.parentElement.insertAdjacentElement('afterend', helpCode);
          }
          btnNextStep[3].disabled = true;
          helpCode.textContent = 'Format: XX-XXX np. 60-200';
          helpCode.style.display = 'block';
        }
      });

      // validate phone input (MK)
      let helpPhone = helpBlock.cloneNode(true)
      formInputs.phone.addEventListener('input', function () {

        if (formInputs.phone.value.trim().length === 9 && parseInt(formInputs.phone.value.trim()) > 0) {
          helpPhone.remove();
        } else {
          if (formInputs.phone.parentElement.nextElementSibling === null) {
            formInputs.phone.parentElement.insertAdjacentElement('afterend', helpPhone);
          }
          btnNextStep[3].disabled = true;
          helpPhone.textContent = 'Numer telefonu musi zawierać 9 cyfr.';
          helpPhone.style.display = 'block';
        }
      });

      // validate date  input (MK)
      // enable possible pick up date starting from tomorrow (MK)
      let today = new Date();
          today = new Date(today.setDate(today.getDate() + 1)).toISOString().split('T')[0];
      formInputs.date.min = today;

      let helpDate = helpBlock.cloneNode(true)
      formInputs.date.addEventListener('input', function () {

        if (formInputs.date.value && formInputs.date.value !== '') {
          helpDate.remove();
        } else {
          if (formInputs.date.parentElement.nextElementSibling === null) {
            formInputs.date.parentElement.insertAdjacentElement('afterend', helpDate);
          }
          btnNextStep[3].disabled = true;
          helpDate.textContent = 'Wybierz datę.';
          helpDate.style.display = 'block';
        }
      });

      // validate time  input (MK)
      let helpTime = helpBlock.cloneNode(true)
      formInputs.time.addEventListener('input', function () {

        if (formInputs.time.value && formInputs.time.value !== '') {
          helpTime.remove();
        } else {
          if (formInputs.time.parentElement.nextElementSibling === null) {
            formInputs.time.parentElement.insertAdjacentElement('afterend', helpTime);
          }
              btnNextStep[3].disabled = true;
          helpTime.textContent = 'Wybierz godzinę.';
          helpTime.style.display = 'block';
        }
      });

      const pickUpInfo = [];
      form.addEventListener('change', function () {
        pickUpInfo.push(formInputs.address, formInputs.city, formInputs.postcode,
            formInputs.phone, formInputs.date, formInputs.time)

        let formFilled = false
        for (let i = 0; i < pickUpInfo.length; i++) {
          if (pickUpInfo[i].value === null || pickUpInfo[i].value === '') {
            break;
          }
          if (i === pickUpInfo.length - 1) {
            formFilled = true
          }
        }

        if (document.querySelector("#error-message") || !formFilled) {
          btnNextStep[3].disabled = true;
        } else {
          btnNextStep[3].disabled = false;
        }
      })
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation
      this.validateForm();

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // getting form inputs (MK)
      const formInputs = this.getFormInputs();

      // changing institutions display based on chosen categories (MK)
      formInputs.categoryCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function () {
          const selectedCategories = Array.from(formInputs.categoryCheckboxes)
              .filter(checkbox => checkbox.checked)
              .map(checkbox => checkbox.value);

          formInputs.institutions.forEach(institution => {
            const institutionCategories = institution.dataset.categories;

            if (selectedCategories.every(category => institutionCategories.includes(category))) {
              institution.parentElement.style.display = "flex";
            } else {
              institution.parentElement.style.display = "none";
            }
          });
        });
      });

      // summary fields (MK)
      const btnNext = document.querySelector("#go_to_summary");
      const bags = document.querySelector(".icon-bag");
      const organization = document.querySelector(".icon-hand");
      const pick_up_address = document.querySelector("#pick_up_address");
      const pick_up_details = document.querySelector("#pick_up_details");

      // changing summary fields inner text for input values (MK)
      btnNext.addEventListener('click', function(){

        // bags  summary (MK)
        let bagsInputValue = parseInt(formInputs.bagsInput.value);
        switch (bagsInputValue) {
                case 1:
                    bags.nextElementSibling.innerText = bagsInputValue + " worek";
                    break;
                case 2:
                case 3:
                case 4:
                    bags.nextElementSibling.innerText = bagsInputValue + " worki";
                    break;
                default:
                    bags.nextElementSibling.innerText = bagsInputValue + " worków";
                    break;
            }

        // institution summary (MK)
        formInputs.institutions.forEach(institution => {
            if (institution.checked) {
              const institutionName = institution.closest('.form-group')
                  .querySelector('.title')
                  .textContent;

              organization.nextElementSibling.innerText = institutionName;
            }
        });

        // pick up address summary (MK)
        const addressData = [];
        addressData.push(formInputs.address, formInputs.city, formInputs.postcode, formInputs.phone);

        const addressLiAll = Array.from(pick_up_address.children);

        addressLiAll.forEach((li, index) => {
          li.innerText = addressData[index].value;
        });

        // pick up details summary (MK)

        // formatting date display (MK)
        const dateObj = new Date(formInputs.date.value);
        const day = dateObj.getDate();
        const month = dateObj.getMonth() + 1;
        const year = dateObj.getFullYear();
        const formattedDate = `${day}/${month}/${year}`

        const more_info = document.querySelector('[name="more_info"]');

        const detailsData = [];
        detailsData.push(formattedDate, formInputs.time.value);

         if (more_info.value.trim() === ''){
          const autoComment = "Brak uwag";
          detailsData.push(autoComment)
        } else {
          detailsData.push(more_info.value);
        }


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

      // getting form data (MK)

      const getForm = document.getElementById('donation_add');
      const formData = new FormData(getForm);
      console.log(...formData)

      //fetching csrf cookie (MK)

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

      // sending form data to server (MK)

      fetch('http://localhost:8000/confirmation/', {
        headers: {
          "X-CSRFToken": cookieValue
        },
        method: 'POST',
        body: formData,
        credentials: "same-origin"
      })

      //     .then(response => response.json())
      //     .then(data => console.log("fromData as quantity" + data))
      //     .catch(error => console.error('Error:', error));
      //     });

      // redirect after form submission (MK)
      window.location.href = "http://localhost:8000/confirmation/"

    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  /**
   * Change color of taken donations in the donations list (MK)
   */
  const rows = document.querySelectorAll('.donation-table tbody tr');

  rows.forEach(row => {
    const tdAll = row.querySelectorAll('td');
    const lastTd = tdAll[tdAll.length - 1];

    if (lastTd.innerText.includes("TAK")) {
      row.style.color = '#D3D3D3';
    }
  });
});
