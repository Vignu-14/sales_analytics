(function () {
  const registry = {};

  function getPalette() {
    const styles = getComputedStyle(document.documentElement);
    return {
      primary: styles.getPropertyValue("--primary").trim() || "#1B2A4A",
      gold: styles.getPropertyValue("--gold").trim() || "#F4B942",
      green: styles.getPropertyValue("--green").trim() || "#2ECC71",
      red: styles.getPropertyValue("--red").trim() || "#E74C3C",
      blue: styles.getPropertyValue("--blue").trim() || "#3498DB",
      slate: "#7F8C8D",
      purple: "#9B59B6",
      teal: "#1ABC9C",
      orange: "#E67E22"
    };
  }

  function formatCurrency(value) {
    return "₹" + Number(value || 0).toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }

  function buildMoneyTick(value) {
    return "₹" + Number(value || 0).toLocaleString("en-IN", {
      maximumFractionDigits: 0
    });
  }

  function destroyChart(canvasId) {
    if (registry[canvasId]) {
      registry[canvasId].destroy();
      delete registry[canvasId];
    }
  }

  function getCanvas(canvasId) {
    const element = document.getElementById(canvasId);
    return element ? element.getContext("2d") : null;
  }

  function createTooltipLabel(context) {
    const label = context.dataset.label ? context.dataset.label + ": " : "";
    return label + formatCurrency(context.raw);
  }

  function createGradientColors(count) {
    const palette = getPalette();
    return Array.from({ length: count }, function (_, index) {
      const alpha = 0.35 + index * (0.5 / Math.max(count, 1));
      return "rgba(52, 152, 219, " + alpha.toFixed(2) + ")";
    });
  }

  function initializeDefaults() {
    if (!window.Chart) {
      return;
    }

    Chart.defaults.font.family = "'Segoe UI', sans-serif";
    Chart.defaults.responsive = true;
    Chart.defaults.maintainAspectRatio = false;
    Chart.defaults.color = "#555555";
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
  }

  function baseAxisOptions(isMoneyAxis) {
    return {
      beginAtZero: true,
      grid: {
        color: "rgba(27, 42, 74, 0.08)"
      },
      ticks: isMoneyAxis
        ? {
            callback: function (value) {
              return buildMoneyTick(value);
            }
          }
        : {}
    };
  }

  function createMonthlySalesChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    const labels = dashboardData.monthlySales.map(function (item) { return item.month; });
    const sales = dashboardData.monthlySales.map(function (item) { return item.sales; });

    registry[canvasId] = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Monthly Sales",
          data: sales,
          borderColor: palette.blue,
          backgroundColor: "rgba(52, 152, 219, 0.16)",
          fill: true,
          pointRadius: 3,
          pointHoverRadius: 5,
          tension: 0.3
        }]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createRegionDoughnutChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: dashboardData.regionData.map(function (item) { return item.region; }),
        datasets: [{
          data: dashboardData.regionData.map(function (item) { return item.sales; }),
          backgroundColor: [palette.primary, palette.gold, palette.green, palette.red, palette.blue],
          borderWidth: 0,
          cutout: "60%"
        }]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        }
      }
    });
  }

  function createRegionComparisonChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.regionData.map(function (item) { return item.region; }),
        datasets: [
          {
            label: "Sales",
            data: dashboardData.regionData.map(function (item) { return item.sales; }),
            backgroundColor: palette.primary
          },
          {
            label: "Profit",
            data: dashboardData.regionData.map(function (item) { return item.profit; }),
            backgroundColor: palette.gold
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createCategoryBarChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.categoryData.map(function (item) { return item.category; }),
        datasets: [
          {
            label: "Sales",
            data: dashboardData.categoryData.map(function (item) { return item.sales; }),
            backgroundColor: palette.blue
          },
          {
            label: "Profit",
            data: dashboardData.categoryData.map(function (item) { return item.profit; }),
            backgroundColor: palette.green
          }
        ]
      },
      options: {
        indexAxis: "y",
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          x: baseAxisOptions(true),
          y: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createSegmentPieChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "pie",
      data: {
        labels: dashboardData.segmentData.map(function (item) { return item.segment; }),
        datasets: [{
          data: dashboardData.segmentData.map(function (item) { return item.sales; }),
          backgroundColor: [palette.blue, palette.gold, palette.green]
        }]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        }
      }
    });
  }

  function createTopProductsChart(canvasId, dataKey) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const dataset = dashboardData[dataKey || "topProducts"] || [];
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dataset.map(function (item) { return item.product; }),
        datasets: [{
          label: "Sales",
          data: dataset.map(function (item) { return item.sales; }),
          backgroundColor: createGradientColors(dataset.length)
        }]
      },
      options: {
        indexAxis: "y",
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          x: baseAxisOptions(true),
          y: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createPaymentChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: dashboardData.paymentData.map(function (item) { return item.method; }),
        datasets: [{
          data: dashboardData.paymentData.map(function (item) { return item.sales; }),
          backgroundColor: [palette.teal, palette.gold, palette.blue, palette.orange, palette.purple],
          borderWidth: 0
        }]
      },
      options: {
        cutout: "60%",
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        }
      }
    });
  }

  function createSalesChannelChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.channelData.map(function (item) { return item.channel; }),
        datasets: [
          {
            label: "Sales",
            data: dashboardData.channelData.map(function (item) { return item.sales; }),
            backgroundColor: palette.blue
          },
          {
            label: "Profit",
            data: dashboardData.channelData.map(function (item) { return item.profit; }),
            backgroundColor: palette.green
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createStateSalesChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.topStates.map(function (item) { return item.state; }),
        datasets: [{
          label: "State Sales",
          data: dashboardData.topStates.map(function (item) { return item.sales; }),
          backgroundColor: palette.purple || "#9B59B6"
        }]
      },
      options: {
        indexAxis: "y",
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          x: baseAxisOptions(true),
          y: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createSubCategoryChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.subCategoryData.map(function (item) { return item.subCategory; }),
        datasets: [{
          label: "Sales",
          data: dashboardData.subCategoryData.map(function (item) { return item.sales; }),
          backgroundColor: createGradientColors(dashboardData.subCategoryData.length)
        }]
      },
      options: {
        indexAxis: "y",
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          x: baseAxisOptions(true),
          y: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createMarginByCategoryChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.marginByCategory.map(function (item) { return item.category; }),
        datasets: [{
          label: "Avg Margin %",
          data: dashboardData.marginByCategory.map(function (item) { return item.avgMargin; }),
          backgroundColor: palette.gold
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return value + "%";
              }
            }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createYearlyComparisonChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.yearlyData.map(function (item) { return item.year; }),
        datasets: [
          {
            label: "Sales",
            data: dashboardData.yearlyData.map(function (item) { return item.sales; }),
            backgroundColor: palette.blue
          },
          {
            label: "Profit",
            data: dashboardData.yearlyData.map(function (item) { return item.profit; }),
            backgroundColor: palette.green
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createQuarterlyChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.quarterlyData.map(function (item) {
          return item.year + " " + item.quarter;
        }),
        datasets: [
          {
            label: "Sales",
            data: dashboardData.quarterlyData.map(function (item) { return item.sales; }),
            backgroundColor: palette.primary
          },
          {
            label: "Profit",
            data: dashboardData.quarterlyData.map(function (item) { return item.profit; }),
            backgroundColor: palette.gold
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createShippingAnalysisChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      data: {
        labels: dashboardData.shipModeData.map(function (item) { return item.mode; }),
        datasets: [
          {
            type: "bar",
            label: "Avg Shipping Days",
            data: dashboardData.shipModeData.map(function (item) { return item.avgDays; }),
            backgroundColor: palette.orange,
            yAxisID: "y"
          },
          {
            type: "line",
            label: "Orders",
            data: dashboardData.shipModeData.map(function (item) { return item.orders; }),
            borderColor: palette.primary,
            backgroundColor: palette.primary,
            yAxisID: "y1",
            tension: 0.3
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                if (context.dataset.label === "Avg Shipping Days") {
                  return context.dataset.label + ": " + Number(context.raw).toFixed(2);
                }
                return context.dataset.label + ": " + Number(context.raw).toLocaleString("en-IN");
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            position: "left"
          },
          y1: {
            beginAtZero: true,
            position: "right",
            grid: { drawOnChartArea: false }
          }
        }
      }
    });
  }

  function createCustomerTypeChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    registry[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: dashboardData.customerTypeData.map(function (item) { return item.type; }),
        datasets: [
          {
            label: "Sales",
            data: dashboardData.customerTypeData.map(function (item) { return item.sales; }),
            backgroundColor: palette.blue
          },
          {
            label: "Profit",
            data: dashboardData.customerTypeData.map(function (item) { return item.profit; }),
            backgroundColor: palette.green
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  function createForecastChart(canvasId) {
    const ctx = getCanvas(canvasId);
    if (!ctx || !window.dashboardData) {
      return;
    }

    destroyChart(canvasId);
    const palette = getPalette();
    const months = dashboardData.forecastData.map(function (item) { return item.month; });
    const confidencePct = (dashboardData.forecastMetrics && dashboardData.forecastMetrics.confidenceBandPct) || 15;
    const predicted = dashboardData.forecastData.map(function (item) { return item.predicted; });
    const lower = predicted.map(function (value) {
      return value == null ? null : Number(value) * (1 - confidencePct / 100);
    });
    const upper = predicted.map(function (value) {
      return value == null ? null : Number(value) * (1 + confidencePct / 100);
    });

    registry[canvasId] = new Chart(ctx, {
      type: "line",
      data: {
        labels: months,
        datasets: [
          {
            label: "Actual Sales",
            data: dashboardData.forecastData.map(function (item) { return item.actual; }),
            borderColor: palette.blue,
            backgroundColor: "rgba(52, 152, 219, 0.12)",
            pointRadius: 3,
            tension: 0.3
          },
          {
            label: "Predicted Sales",
            data: predicted,
            borderColor: palette.orange,
            backgroundColor: "rgba(230, 126, 34, 0.12)",
            borderDash: [6, 4],
            pointRadius: 3,
            tension: 0.3
          },
          {
            label: "Lower Band",
            data: lower,
            borderColor: "rgba(230, 126, 34, 0)",
            pointRadius: 0,
            fill: false
          },
          {
            label: "Confidence Band",
            data: upper,
            borderColor: "rgba(230, 126, 34, 0)",
            backgroundColor: "rgba(230, 126, 34, 0.14)",
            pointRadius: 0,
            fill: "-1"
          }
        ]
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              label: createTooltipLabel
            }
          }
        },
        scales: {
          y: baseAxisOptions(true),
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  window.DashboardCharts = {
    formatCurrency: formatCurrency,
    initializeDefaults: initializeDefaults,
    createMonthlySalesChart: createMonthlySalesChart,
    createRegionDoughnutChart: createRegionDoughnutChart,
    createRegionComparisonChart: createRegionComparisonChart,
    createCategoryBarChart: createCategoryBarChart,
    createSegmentPieChart: createSegmentPieChart,
    createTopProductsChart: createTopProductsChart,
    createPaymentChart: createPaymentChart,
    createSalesChannelChart: createSalesChannelChart,
    createStateSalesChart: createStateSalesChart,
    createSubCategoryChart: createSubCategoryChart,
    createMarginByCategoryChart: createMarginByCategoryChart,
    createYearlyComparisonChart: createYearlyComparisonChart,
    createQuarterlyChart: createQuarterlyChart,
    createShippingAnalysisChart: createShippingAnalysisChart,
    createCustomerTypeChart: createCustomerTypeChart,
    createForecastChart: createForecastChart
  };

  document.addEventListener("DOMContentLoaded", initializeDefaults);
})();
