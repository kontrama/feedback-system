document.addEventListener('DOMContentLoaded', function() {
            function animateOnScroll() {
                const elements = document.querySelectorAll('.animate-on-scroll');
                elements.forEach(element => {
                    const elementPosition = element.getBoundingClientRect().top;
                    const screenPosition = window.innerHeight / 1.2;
                    if (elementPosition < screenPosition) {
                        element.classList.add('visible');
                    }
                });
            }
            animateOnScroll();
            window.addEventListener('scroll', animateOnScroll);
        });