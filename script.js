// Tatvam Tools - Main JavaScript

// Load navbar and footer components
async function loadComponents() {
    // Load navbar
    const navbarPlaceholder = document.getElementById('navbar-placeholder');
    if (navbarPlaceholder) {
        try {
            const response = await fetch('components/navbar.html');
            if (response.ok) {
                const html = await response.text();
                navbarPlaceholder.innerHTML = html;
                initNavbar();
            }
        } catch (e) {
            console.log('Navbar component not found, using inline navbar');
        }
    }

    // Load footer
    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) {
        try {
            const response = await fetch('components/footer.html');
            if (response.ok) {
                const html = await response.text();
                footerPlaceholder.innerHTML = html;
            }
        } catch (e) {
            console.log('Footer component not found, using inline footer');
        }
    }
}

// Initialize navbar functionality
function initNavbar() {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function () {
            this.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
            if (navLinks) navLinks.classList.remove('active');
        });
    });

    // Set active nav link based on current page
    setActiveNavLink();
}

// Set the active navigation link based on current URL
function setActiveNavLink() {
    const pathname = window.location.pathname;
    const currentPage = pathname.split('/').pop() || 'index.html';
    // Remove .html extension for comparison
    const pageWithoutExt = currentPage.replace('.html', '');
    const navLinksItems = document.querySelectorAll('.nav-link');

    navLinksItems.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        const hrefWithoutExt = href.replace('.html', '');

        // Match if: exact match, or root path matches index, or names match without extension
        if (href === currentPage ||
            hrefWithoutExt === pageWithoutExt ||
            (currentPage === '' && href === 'index.html') ||
            (pageWithoutExt === '' && hrefWithoutExt === 'index') ||
            (pathname === '/' && href === 'index.html')) {
            link.classList.add('active');
        }
    });
}

// Load components first, then initialize
loadComponents();

document.addEventListener('DOMContentLoaded', function () {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function () {
            this.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuBtn.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });

    // Header scroll effect
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }


        lastScroll = currentScroll;
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                // Update active state on click
                updateActiveNavLink(this.getAttribute('href').substring(1));
            }
        });
    });

    // Scroll Spy - Highlight current section in navbar
    const sections = document.querySelectorAll('section[id]');
    const navLinksForSpy = document.querySelectorAll('.nav-link');

    function updateActiveNavLink(sectionId) {
        navLinksForSpy.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `#${sectionId}` || href === `index.html#${sectionId}` ||
                (sectionId === 'hero' && (href === 'index.html' || href === '#'))) {
                link.classList.add('active');
            }
        });
    }

    function scrollSpy() {
        const scrollPosition = window.scrollY + 150; // Offset for header

        // Check if at top of page (hero section)
        if (scrollPosition < 300) {
            navLinksForSpy.forEach(link => link.classList.remove('active'));
            const homeLink = document.querySelector('.nav-link[href="index.html"]') ||
                document.querySelector('.nav-link[href="#"]');
            if (homeLink) homeLink.classList.add('active');
            return;
        }

        // Find current section
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                updateActiveNavLink(sectionId);
            }
        });
    }

    // Get current page name for detection (handle both .html and non-.html URLs)
    const pathname = window.location.pathname;
    const currentPageName = pathname.split('/').pop().replace('.html', '') || 'index';

    // Check if on specific pages
    const isContactPage = currentPageName === 'contact';
    const isAboutPage = currentPageName === 'about';
    const isProductsPage = currentPageName === 'products';
    const isHomePage = currentPageName === 'index' || currentPageName === '' || pathname === '/';

    if (isContactPage) {
        // On contact page - always highlight Contact link
        navLinksForSpy.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes('contact')) {
                link.classList.add('active');
            }
        });
    } else if (isAboutPage) {
        // On about page - always highlight About Us link
        navLinksForSpy.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes('about')) {
                link.classList.add('active');
            }
        });
    } else if (isProductsPage) {
        // On products page - always highlight Products link
        navLinksForSpy.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').includes('products')) {
                link.classList.add('active');
            }
        });
    } else if (isHomePage) {
        // On main page - run scroll spy
        window.addEventListener('scroll', scrollSpy);
        scrollSpy(); // Initial call
    }

    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .product-showcase, .application-item, .spec-row').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add animate-in styles
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // Contact Form Handling
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Get form data
            const formData = new FormData(this);
            const data = Object.fromEntries(formData.entries());

            // Basic validation
            if (!data.name || !data.email || !data.subject || !data.message) {
                showNotification('Please fill in all required fields.', 'error');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(data.email)) {
                showNotification('Please enter a valid email address.', 'error');
                return;
            }

            // Simulate form submission
            const submitBtn = this.querySelector('.submit-btn');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span>Sending...</span>';
            submitBtn.disabled = true;

            // Simulate API call
            setTimeout(() => {
                showNotification('Thank you! Your message has been sent successfully. We will get back to you soon.', 'success');
                contactForm.reset();
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 1500);
        });
    }

    // Notification function
    function showNotification(message, type) {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${type === 'success' ? '✓' : '✕'}</span>
                <span class="notification-message">${message}</span>
            </div>
            <button class="notification-close" onclick="this.parentElement.remove()">×</button>
        `;

        // Add styles
        const notificationStyles = document.createElement('style');
        notificationStyles.textContent = `
            .notification {
                position: fixed;
                top: 100px;
                right: 20px;
                max-width: 400px;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                z-index: 10000;
                animation: slideIn 0.3s ease;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            .notification-success {
                background: linear-gradient(135deg, #00a759 0%, #00c96b 100%);
                color: white;
            }
            .notification-error {
                background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
                color: white;
            }
            .notification-content {
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            .notification-icon {
                font-size: 1.25rem;
                font-weight: bold;
            }
            .notification-message {
                font-size: 0.95rem;
                line-height: 1.4;
            }
            .notification-close {
                background: none;
                border: none;
                color: white;
                font-size: 1.5rem;
                cursor: pointer;
                opacity: 0.8;
                transition: opacity 0.2s;
            }
            .notification-close:hover {
                opacity: 1;
            }
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(notificationStyles);

        // Add notification to page
        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.style.animation = 'slideIn 0.3s ease reverse';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }

    // Product card hover effect enhancement
    document.querySelectorAll('.product-card').forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Stats counter animation
    function animateCounter(element, target, suffix = '', duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);

        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target + suffix;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start) + suffix;
            }
        }, 16);
    }

    // Animate stats when in view
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const statNumber = entry.target.querySelector('.stat-number');
                if (statNumber) {
                    const text = statNumber.textContent;
                    // Extract number and suffix (e.g., "90°C" -> 90 and "°C", "50+" -> 50 and "+")
                    const match = text.match(/^(\d+)(.*)$/);
                    if (match) {
                        const value = parseInt(match[1]);
                        const suffix = match[2] || '';
                        animateCounter(statNumber, value, suffix);
                    }
                }
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.stat-item').forEach(stat => {
        statsObserver.observe(stat);
    });

    // Add ripple effect to buttons
    document.querySelectorAll('.btn-primary, .btn-secondary, .btn-outline, .submit-btn').forEach(button => {
        button.addEventListener('click', function (e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;

            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add ripple animation
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);

    console.log('Tatvam Tools website loaded successfully!');
});

// Product gallery image change function
function changeImage(thumb) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage && thumb) {
        mainImage.src = thumb.src;
        // Update active state
        document.querySelectorAll('.gallery-thumbs .thumb').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
    }
}
