document.addEventListener('DOMContentLoaded', () => {
  const resetBtn = document.getElementById('reset');
  const form = document.getElementById('my_form');
  const mainElements = document.getElementsByTagName('main');
  const downloadBtn = document.getElementById('download');
  const dbBtn = document.getElementById('database');

  // if (weatherData && Object.keys(weatherData).length > 0) {
  //   dbBtn.removeAttribute('disabled');
  // }

  resetBtn.addEventListener('click', () => {
    if (mainElements.length > 0) {
      const main = mainElements[0];
      main.style.display = 'none';
      removeAllChildren(main);
    }
  });

  const loader = document.getElementById('loader');
  form.addEventListener('submit', () => {
    loader.style.display = 'flex';
    if (mainElements.length > 0) {
      const main = mainElements[0];
      main.style.display = 'none';
      removeAllChildren(main);
    }
  });

  dbBtn.addEventListener('click', (e) => {
    e.preventDefault();
    fetch('/push_to_db', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(weatherData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then((data) => {
        Swal.fire({
          icon: 'success',
          title: 'Successfully uploaded to DynamoDB',
          showConfirmButton: false,
          timer: 1500,
        });
        console.log('Success:', data);
      })
      .catch((error) => {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Something went wrong!',
        });
        console.error('Error:', error);
      });
  });

  downloadBtn.addEventListener('click', function (event) {
    event.preventDefault();

    const imageUrl = 'https://bucket-html.s3.amazonaws.com/Sky.jpg';

    fetch(imageUrl)
      .then((response) => response.blob())
      .then((blob) => {
        const blobUrl = URL.createObjectURL(blob);

        const tempLink = document.createElement('a');
        tempLink.href = blobUrl;
        tempLink.download = 'Sky.jpg';
        document.body.appendChild(tempLink);

        tempLink.click();

        // Clean up and remove the temporary link
        document.body.removeChild(tempLink);
        URL.revokeObjectURL(blobUrl);
      })
      .catch((error) => console.error('Download failed:', error));
  });
});

function removeAllChildren(element) {
  while (element.firstChild) {
    element.removeChild(element.firstChild);
  }
}
