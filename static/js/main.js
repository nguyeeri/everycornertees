// ── File upload handling ──
const uploadArea   = document.getElementById('upload-area');
const uploadInput  = document.getElementById('designs');
const uploadTrigger= document.getElementById('upload-trigger');
const fileList     = document.getElementById('file-list');
let selectedFiles  = [];

uploadTrigger.addEventListener('click', () => uploadInput.click());

uploadArea.addEventListener('dragover', e => {
  e.preventDefault();
  uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));

uploadArea.addEventListener('drop', e => {
  e.preventDefault();
  uploadArea.classList.remove('dragover');
  addFiles(Array.from(e.dataTransfer.files));
});

uploadInput.addEventListener('change', () => {
  addFiles(Array.from(uploadInput.files));
  uploadInput.value = '';
});

function addFiles(newFiles) {
  newFiles.forEach(f => {
    if (!selectedFiles.find(x => x.name === f.name && x.size === f.size)) {
      selectedFiles.push(f);
    }
  });
  renderFileList();
}

function removeFile(index) {
  selectedFiles.splice(index, 1);
  renderFileList();
}

function renderFileList() {
  fileList.innerHTML = '';
  selectedFiles.forEach((f, i) => {
    const item = document.createElement('div');
    item.className = 'file-item';
    const kb = (f.size / 1024).toFixed(0);
    const size = f.size > 1024 * 1024
      ? (f.size / (1024 * 1024)).toFixed(1) + ' MB'
      : kb + ' KB';
    item.innerHTML = `<span>${f.name} <span style="color:#bbb">(${size})</span></span>
      <button class="file-remove" type="button" onclick="removeFile(${i})">×</button>`;
    fileList.appendChild(item);
  });
}

// ── Form submission ──
const form       = document.getElementById('quote-form');
const submitBtn  = document.getElementById('submit-btn');
const successMsg = document.getElementById('form-success');
const errorMsg   = document.getElementById('form-error');

form.addEventListener('submit', async e => {
  e.preventDefault();

  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending…';
  successMsg.style.display = 'none';
  errorMsg.style.display   = 'none';

  const fd = new FormData(form);

  // Remove default file input and add our tracked files
  fd.delete('designs');
  selectedFiles.forEach(f => fd.append('designs', f));

  try {
    const res  = await fetch('/submit', { method: 'POST', body: fd });
    const data = await res.json();

    if (data.success) {
      successMsg.style.display = 'block';
      form.reset();
      selectedFiles = [];
      renderFileList();
      successMsg.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } else {
      errorMsg.style.display = 'block';
    }
  } catch {
    errorMsg.style.display = 'block';
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Send quote request →';
  }
});

// ── Smooth nav highlight ──
const quoteSection = document.getElementById('quote');
const navCta = document.querySelector('.nav-cta');

const observer = new IntersectionObserver(entries => {
  navCta.style.background = entries[0].isIntersecting ? '#d4410a' : '';
}, { threshold: 0.2 });

if (quoteSection) observer.observe(quoteSection);
