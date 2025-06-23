document.addEventListener('DOMContentLoaded', () => {
  const rows = Array.from(document.querySelectorAll('table.products-table tbody tr'))
    .filter(r => r.dataset.id);
  const products = rows.map(r => {
    const cells = r.querySelectorAll('td');
    return {
      price: parseFloat(cells[2].textContent) || 0,
      discounted: parseFloat(cells[3].textContent) || 0,
      rating: parseFloat(cells[4].textContent) || 0
    };
  });

  if (products.length === 0) return;

  function buildPriceHistogram(ctx, data, binCount = 10) {
    const prices = data.map(p => p.price);
    const min = Math.min(...prices);
    const max = Math.max(...prices);
    const binSize = (max - min) / binCount;

    const bins = Array(binCount).fill(0);
    prices.forEach(price => {
      let idx = Math.floor((price - min) / binSize);
      if (idx === binCount) idx = binCount - 1;
      bins[idx]++;
    });

    const labels = bins.map((_, i) => {
      const start = (min + i * binSize).toFixed(0);
      const end = (min + (i + 1) * binSize).toFixed(0);
      return `${start}–${end}`;
    });

    return new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Количество товаров',
          data: bins
        }]
      },
      options: {
        scales: {
          x: { title: { display: true, text: 'Диапазон цен, ₽' } },
          y: { title: { display: true, text: 'Количество товаров' }, beginAtZero: true }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.parsed.y} товара(ов)`
            }
          }
        }
      }
    });
  }


  function buildDiscountRatingChart(ctx, data) {

    const sorted = data.slice().sort((a, b) => a.rating - b.rating);
    return new Chart(ctx, {
      type: 'line',
      data: {
        labels: sorted.map(p => p.rating.toFixed(1)),
        datasets: [{
          label: 'Скидка (₽)',
          data: sorted.map(p => p.discounted),
          fill: false,
          tension: 0.2,
          pointRadius: 4
        }]
      },
      options: {
        scales: {
          x: { title: { display: true, text: 'Рейтинг' } },
          y: { title: { display: true, text: 'Скидка, ₽' }, beginAtZero: true }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: ctx => `Рейтинг ${ctx.label}: скидка ${ctx.parsed.y}₽`
            }
          }
        }
      }
    });
  }


  const priceCtx = document.getElementById('priceHistogram').getContext('2d');
  const discountCtx = document.getElementById('discountRatingChart').getContext('2d');


  buildPriceHistogram(priceCtx, products);
  buildDiscountRatingChart(discountCtx, products);
});