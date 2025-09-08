// Enclave Messenger Demo Application JavaScript

// Global state
let currentKeys = {
    publicKey: '',
    privateKey: '',
    aesKey: '',
    encryptedMessage: '',
    encryptedAESKey: ''
};

let konamiSequence = [
    'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
    'KeyB', 'KeyA'
];
let konamiProgress = [];

// Easter egg responses
const easterEggs = {
    '/joke': [
        'Why don\'t programmers like nature? Too many bugs! 🐛',
        'How many programmers does it take to change a light bulb? None, that\'s a hardware problem! 💡',
        'Why do programmers prefer dark mode? Because light attracts bugs! 🌙',
        'What\'s a programmer\'s favorite hangout place? The Foo Bar! 🍺',
        'Why did the programmer quit his job? He didn\'t get arrays! 📊'
    ],
    '/ascii': [
        '( ͡° ͜ʖ ͡°)',
        '┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻',
        '🔐 ENCRYPTED ASCII ART 🔐\n░░░▓▓▓░░░\n░▓▓▓▓▓▓▓░\n▓▓▓▓▓▓▓▓▓\n░▓▓▓▓▓▓▓░\n░░░▓▓▓░░░',
        '    /\\_/\\  \n   ( o.o ) \n    > ^ <',
        '┌─┐┬ ┬┌─┐┬─┐\n├─┤├─┤├┤ ├┬┘\n┴ ┴┴ ┴└─┘┴└─'
    ],
    '/boom': [
        '💥✨🔥💣⚡🌟💫🎆',
        '💥 BOOM! 💥\n🎇✨🎆✨🎇\n💫⚡💫⚡💫\n🔥🌟🔥🌟🔥',
        '🚀💥 EXPLOSIVE ENCRYPTION! 💥🚀\n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡\n🔥 Messages secured with a BANG! 🔥'
    ],
    '/matrix': [
        '🔋 ENTERING THE MATRIX...\n01001000 01100101 01101100 01101100 01101111\n🔐 Reality is just encrypted data 🔐\n💊 Take the red pill for ultimate security 💊'
    ],
    '/konami': [
        '🎮 KONAMI CODE ACTIVATED!\n🚀 CHEAT MODE ENABLED 🚀\n🔓 All encryption algorithms unlocked!\n✨ You are now a crypto wizard! ✨'
    ]
};

// Programming jokes for random selection
const jokes = easterEggs['/joke'];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initEncryptionDemo();
    initInterfaceTabs();
    initEasterEggs();
    initKonamiCode();
    initCopyButtons();
    initTerminalSimulation();
    
    console.log('🔐 Enclave Messenger Demo initialized');
});

// Navigation functionality
function initNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const sectionName = tab.dataset.section;
            showSection(sectionName);
            
            // Update active tab
            navTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });
}

function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Show target section
    const targetSection = document.getElementById(sectionName);
    if (targetSection) {
        targetSection.classList.add('active');
    }
    
    // Update nav tabs
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.section === sectionName) {
            tab.classList.add('active');
        }
    });
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Encryption demo functionality
function initEncryptionDemo() {
    const generateKeysBtn = document.getElementById('generateKeys');
    const encryptMessageBtn = document.getElementById('encryptMessage');
    const decryptMessageBtn = document.getElementById('decryptMessage');
    
    if (generateKeysBtn) {
        generateKeysBtn.addEventListener('click', generateKeys);
    }
    
    if (encryptMessageBtn) {
        encryptMessageBtn.addEventListener('click', encryptMessage);
    }
    
    if (decryptMessageBtn) {
        decryptMessageBtn.addEventListener('click', decryptMessage);
    }
}

function generateKeys() {
    // Simulate key generation
    const keyDisplay = document.getElementById('keyDisplay');
    const publicKeyEl = document.getElementById('publicKey');
    const privateKeyEl = document.getElementById('privateKey');
    
    // Generate mock RSA keys
    const mockPublicKey = generateMockKey('PUBLIC');
    const mockPrivateKey = generateMockKey('PRIVATE');
    
    currentKeys.publicKey = mockPublicKey;
    currentKeys.privateKey = mockPrivateKey;
    
    publicKeyEl.textContent = mockPublicKey;
    privateKeyEl.textContent = mockPrivateKey;
    
    keyDisplay.style.display = 'block';
    
    // Animate the flow steps
    animateFlowStep(1);
    
    // Enable encryption button
    const encryptBtn = document.getElementById('encryptMessage');
    if (encryptBtn) {
        encryptBtn.disabled = false;
    }
}

function generateMockKey(type) {
    const prefix = type === 'PUBLIC' ? '-----BEGIN PUBLIC KEY-----' : '-----BEGIN PRIVATE KEY-----';
    const suffix = type === 'PUBLIC' ? '-----END PUBLIC KEY-----' : '-----END PRIVATE KEY-----';
    
    let keyContent = '';
    for (let i = 0; i < 4; i++) {
        keyContent += '\n' + Array.from({length: 64}, () => 
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
            [Math.floor(Math.random() * 64)]
        ).join('');
    }
    
    return prefix + keyContent + '\n' + suffix;
}

function encryptMessage() {
    const plainMessage = document.getElementById('plainMessage').value;
    const encryptionResult = document.getElementById('encryptionResult');
    const encryptedMessageEl = document.getElementById('encryptedMessage');
    const encryptedAESKeyEl = document.getElementById('encryptedAESKey');
    
    if (!plainMessage) {
        alert('Please enter a message to encrypt!');
        return;
    }
    
    if (!currentKeys.publicKey) {
        alert('Please generate keys first!');
        return;
    }
    
    // Simulate encryption
    const mockAESKey = generateRandomHex(64);
    const mockEncryptedMessage = btoa(plainMessage).replace(/[=]/g, '').replace(/[+]/g, '-').replace(/[/]/g, '_') + generateRandomHex(32);
    const mockEncryptedAESKey = generateRandomHex(512);
    
    currentKeys.aesKey = mockAESKey;
    currentKeys.encryptedMessage = mockEncryptedMessage;
    currentKeys.encryptedAESKey = mockEncryptedAESKey;
    
    encryptedMessageEl.textContent = mockEncryptedMessage;
    encryptedAESKeyEl.textContent = mockEncryptedAESKey;
    
    encryptionResult.style.display = 'block';
    
    // Animate flow steps
    animateFlowStep(2);
    setTimeout(() => animateFlowStep(3), 500);
    setTimeout(() => animateFlowStep(4), 1000);
    
    // Enable decrypt button
    const decryptBtn = document.getElementById('decryptMessage');
    if (decryptBtn) {
        decryptBtn.disabled = false;
    }
}

function decryptMessage() {
    const decryptionResult = document.getElementById('decryptionResult');
    const decryptedTextEl = document.getElementById('decryptedText');
    const originalMessage = document.getElementById('plainMessage').value;
    
    if (!currentKeys.encryptedMessage) {
        alert('Please encrypt a message first!');
        return;
    }
    
    // Simulate decryption
    decryptedTextEl.textContent = originalMessage;
    decryptionResult.style.display = 'block';
    
    // Add success animation
    decryptedTextEl.classList.add('boom-effect');
    setTimeout(() => decryptedTextEl.classList.remove('boom-effect'), 1000);
}

function generateRandomHex(length) {
    return Array.from({length}, () => 
        Math.floor(Math.random() * 16).toString(16)
    ).join('');
}

function animateFlowStep(stepNumber) {
    // Remove active class from all steps
    const steps = document.querySelectorAll('.flow-step');
    steps.forEach(step => step.classList.remove('active'));
    
    // Add active class to current step
    const currentStep = document.getElementById(`step${stepNumber}`);
    if (currentStep) {
        currentStep.classList.add('active');
    }
}

// Interface tabs functionality
function initInterfaceTabs() {
    const interfaceTabs = document.querySelectorAll('.interface-tab');
    
    interfaceTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const interfaceName = tab.dataset.interface;
            showInterface(interfaceName);
            
            // Update active tab
            interfaceTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        });
    });
}

function showInterface(interfaceName) {
    // Hide all interface contents
    const contents = document.querySelectorAll('.interface-content');
    contents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Show target interface
    const targetContent = document.getElementById(`${interfaceName}-interface`);
    if (targetContent) {
        targetContent.classList.add('active');
    }
}

// Easter eggs functionality
function initEasterEggs() {
    const easterEggInput = document.getElementById('easterEggInput');
    const executeBtn = document.querySelector('#easter-eggs .btn--primary');
    
    if (easterEggInput && executeBtn) {
        executeBtn.addEventListener('click', executeEasterEgg);
        
        easterEggInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                executeEasterEgg();
            }
        });
    }
}

function executeEasterEgg() {
    const input = document.getElementById('easterEggInput');
    const output = document.getElementById('commandOutput');
    const command = input.value.trim().toLowerCase();
    
    if (!command) return;
    
    let response = '';
    
    if (easterEggs[command]) {
        if (command === '/joke') {
            response = jokes[Math.floor(Math.random() * jokes.length)];
        } else {
            const responses = easterEggs[command];
            response = responses[Math.floor(Math.random() * responses.length)];
        }
        
        // Special effects for certain commands
        if (command === '/matrix') {
            output.classList.add('matrix-effect');
            setTimeout(() => output.classList.remove('matrix-effect'), 3000);
        } else if (command === '/boom') {
            output.classList.add('boom-effect');
            setTimeout(() => output.classList.remove('boom-effect'), 1000);
        }
    } else {
        response = `Unknown command: ${command}\nTry: /joke, /ascii, /boom, /matrix, /konami`;
    }
    
    // Type writer effect
    output.textContent = '';
    typeWriter(output, response, 50);
    
    input.value = '';
}

function showEggExample(command) {
    const input = document.getElementById('easterEggInput');
    const output = document.getElementById('commandOutput');
    
    input.value = command;
    
    let response = '';
    if (easterEggs[command]) {
        if (command === '/joke') {
            response = jokes[Math.floor(Math.random() * jokes.length)];
        } else {
            const responses = easterEggs[command];
            response = responses[Math.floor(Math.random() * responses.length)];
        }
        
        // Special effects
        if (command === '/matrix') {
            output.classList.add('matrix-effect');
            setTimeout(() => output.classList.remove('matrix-effect'), 3000);
        } else if (command === '/boom') {
            output.classList.add('boom-effect');
            setTimeout(() => output.classList.remove('boom-effect'), 1000);
        }
    }
    
    typeWriter(output, response, 30);
}

function typeWriter(element, text, speed = 50) {
    element.textContent = '';
    let i = 0;
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Konami code functionality
function initKonamiCode() {
    document.addEventListener('keydown', handleKonamiInput);
}

function handleKonamiInput(event) {
    konamiProgress.push(event.code);
    
    // Keep only the last 10 keys
    if (konamiProgress.length > konamiSequence.length) {
        konamiProgress.shift();
    }
    
    // Update progress display
    updateKonamiProgress();
    
    // Check if sequence matches
    if (konamiProgress.length === konamiSequence.length) {
        const matches = konamiProgress.every((key, index) => key === konamiSequence[index]);
        
        if (matches) {
            activateKonamiCode();
            konamiProgress = [];
        }
    }
}

function updateKonamiProgress() {
    const progressEl = document.getElementById('konamiProgress');
    if (!progressEl) return;
    
    const symbols = {
        'ArrowUp': '↑',
        'ArrowDown': '↓',
        'ArrowLeft': '←',
        'ArrowRight': '→',
        'KeyB': 'B',
        'KeyA': 'A'
    };
    
    progressEl.textContent = konamiProgress
        .map(key => symbols[key] || '?')
        .join(' ');
}

function activateKonamiCode() {
    const progressEl = document.getElementById('konamiProgress');
    const output = document.getElementById('commandOutput');
    
    // Show success message
    if (progressEl) {
        progressEl.textContent = '🎮 KONAMI CODE ACTIVATED! 🎮';
        progressEl.style.color = '#00ff00';
        progressEl.style.textShadow = '0 0 10px #00ff00';
    }
    
    // Show easter egg response
    if (output) {
        const response = easterEggs['/konami'][0];
        typeWriter(output, response, 30);
        
        // Add special effects
        output.classList.add('matrix-effect');
        setTimeout(() => output.classList.remove('matrix-effect'), 3000);
    }
    
    // Reset progress after animation
    setTimeout(() => {
        if (progressEl) {
            progressEl.textContent = '';
            progressEl.style.color = '';
            progressEl.style.textShadow = '';
        }
    }, 5000);
    
    // Add temporary body effect
    document.body.style.animation = 'boom 0.5s ease-out';
    setTimeout(() => {
        document.body.style.animation = '';
    }, 500);
}

// Copy functionality for code blocks
function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(btn => {
        btn.addEventListener('click', () => copyCode(btn));
    });
}

function copyCode(button) {
    const codeBlock = button.parentElement;
    const codeText = codeBlock.querySelector('code').textContent;
    
    navigator.clipboard.writeText(codeText).then(() => {
        // Show success feedback
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.classList.add('copy-success');
        
        setTimeout(() => {
            button.textContent = originalText;
            button.classList.remove('copy-success');
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy code: ', err);
        alert('Failed to copy code. Please select and copy manually.');
    });
}

// Terminal simulation
function initTerminalSimulation() {
    const terminal = document.getElementById('terminal-output');
    if (!terminal) return;
    
    // Add some interactive terminal commands
    setTimeout(() => {
        addTerminalLine('enclave> /status');
        setTimeout(() => {
            addTerminalLine('🔐 Encryption: Active (RSA-2048 + AES-256)', 'output');
            addTerminalLine('🛡️ P2P Connection: Established', 'output');
            addTerminalLine('👥 Active Users: 2', 'output');
            addTerminalLine('📊 Messages Encrypted: 1,337', 'output');
        }, 1000);
    }, 3000);
}

function addTerminalLine(text, className = '') {
    const terminal = document.getElementById('terminal-output');
    if (!terminal) return;
    
    const line = document.createElement('div');
    line.className = `terminal-line ${className}`;
    line.textContent = text;
    
    // Remove cursor from last line
    const lastLine = terminal.querySelector('.terminal-line:last-child');
    if (lastLine) {
        lastLine.innerHTML = lastLine.innerHTML.replace('<span class="cursor">|</span>', '');
    }
    
    terminal.appendChild(line);
    
    // Add cursor to new line if it's a prompt
    if (!className && text.includes('enclave>')) {
        const cursor = document.createElement('span');
        cursor.className = 'cursor';
        cursor.textContent = '|';
        line.appendChild(cursor);
    }
    
    // Auto scroll terminal
    terminal.scrollTop = terminal.scrollHeight;
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Performance monitoring
function logPerformance(label, startTime) {
    const endTime = performance.now();
    console.log(`${label}: ${endTime - startTime} milliseconds`);
}

// Initialize intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for scroll animations
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.feature-card, .demo-step, .layer, .step');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Export functions for global access
window.showSection = showSection;
window.executeEasterEgg = executeEasterEgg;
window.showEggExample = showEggExample;
window.copyCode = copyCode;