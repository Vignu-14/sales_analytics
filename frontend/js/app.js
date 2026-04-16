(function () {
  function formatCurrency(value) {
    return "₹" + Number(value || 0).toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }

  function formatNumber(value) {
    return Number(value || 0).toLocaleString("en-IN");
  }

  function formatPercentage(value) {
    return Number(value || 0).toLocaleString("en-IN", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }) + "%";
  }

  function getPage() {
    return document.body.dataset.page || "dashboard";
  }

  function setActiveSidebarLink() {
    const page = getPage();
    document.querySelectorAll(".nav-link").forEach(function (link) {
      link.classList.toggle("active", link.dataset.pageLink === page);
    });
  }

  function setupIntersectionObserver() {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
        }
      });
    }, { threshold: 0.15 });

    document.querySelectorAll(".observer-item").forEach(function (item) {
      observer.observe(item);
    });
  }

  function setupSidebarToggle() {
    const button = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");
    if (!button || !sidebar) {
      return;
    }

    button.addEventListener("click", function () {
      sidebar.classList.toggle("open");
    });
  }

  function populateKPIs() {
    if (!window.dashboardData || !dashboardData.overallKPIs) {
      return;
    }

    const kpis = dashboardData.overallKPIs;
    const mapping = {
      totalSales: formatCurrency(kpis.totalSales),
      totalProfit: formatCurrency(kpis.totalProfit),
      totalOrders: formatNumber(kpis.totalOrders),
      profitMargin: formatPercentage(kpis.profitMargin),
      avgOrderValue: formatCurrency(kpis.avgOrderValue),
      totalCustomers: formatNumber(kpis.totalCustomers)
    };

    Object.keys(mapping).forEach(function (key) {
      const valueElement = document.querySelector("[data-kpi-value='" + key + "']");
      if (!valueElement) {
        return;
      }

      valueElement.textContent = mapping[key];
      if (key === "totalProfit") {
        valueElement.classList.add(Number(kpis.totalProfit) >= 0 ? "positive" : "negative");
      }
    });
  }

  function renderTableBody(tableId, rows, columns) {
    const body = document.querySelector("#" + tableId + " tbody");
    if (!body) {
      return;
    }

    body.innerHTML = rows.map(function (row) {
      const cells = columns.map(function (column) {
        const value = typeof column.render === "function" ? column.render(row) : row[column.key];
        return "<td>" + value + "</td>";
      }).join("");
      return "<tr>" + cells + "</tr>";
    }).join("");
  }

  function makeTablesSortable() {
    document.querySelectorAll("table[data-sortable='true']").forEach(function (table) {
      table.querySelectorAll("th[data-sort-key]").forEach(function (header) {
        header.addEventListener("click", function () {
          const key = header.dataset.sortKey;
          const tbody = table.querySelector("tbody");
          const rows = Array.from(tbody.querySelectorAll("tr"));
          const ascending = header.dataset.order !== "asc";
          header.dataset.order = ascending ? "asc" : "desc";

          rows.sort(function (rowA, rowB) {
            const valueA = rowA.querySelector("[data-key='" + key + "']") || rowA.children[header.cellIndex];
            const valueB = rowB.querySelector("[data-key='" + key + "']") || rowB.children[header.cellIndex];
            const parsedA = parseFloat(String(valueA.textContent).replace(/[₹,%\s,]/g, ""));
            const parsedB = parseFloat(String(valueB.textContent).replace(/[₹,%\s,]/g, ""));

            if (!Number.isNaN(parsedA) && !Number.isNaN(parsedB)) {
              return ascending ? parsedA - parsedB : parsedB - parsedA;
            }

            return ascending
              ? valueA.textContent.localeCompare(valueB.textContent)
              : valueB.textContent.localeCompare(valueA.textContent);
          });

          rows.forEach(function (row) {
            tbody.appendChild(row);
          });
        });
      });
    });
  }

  function renderDashboardPage() {
    populateKPIs();
    DashboardCharts.createMonthlySalesChart("monthlySalesChart");
    DashboardCharts.createRegionDoughnutChart("regionSalesChart");
    DashboardCharts.createCategoryBarChart("categoryChart");
    DashboardCharts.createSegmentPieChart("segmentChart");
    DashboardCharts.createTopProductsChart("topProductsChart", "topProducts");
    DashboardCharts.createPaymentChart("paymentChart");
    DashboardCharts.createSalesChannelChart("salesChannelChart");
  }

  function renderRegionalPage() {
    DashboardCharts.createRegionComparisonChart("regionalBreakdownChart");
    DashboardCharts.createStateSalesChart("stateSalesChart");

    renderTableBody("regionTable", dashboardData.regionData, [
      { key: "region" },
      { key: "sales", render: function (row) { return formatCurrency(row.sales); } },
      { key: "profit", render: function (row) { return formatCurrency(row.profit); } },
      { key: "orders", render: function (row) { return formatNumber(row.orders); } }
    ]);

    renderTableBody("cityTable", dashboardData.cityData, [
      { key: "city" },
      { key: "state" },
      { key: "region" },
      { key: "sales", render: function (row) { return formatCurrency(row.sales); } },
      { key: "profit", render: function (row) { return formatCurrency(row.profit); } },
      { key: "orders", render: function (row) { return formatNumber(row.orders); } }
    ]);
  }

  function renderProductsPage() {
    DashboardCharts.createCategoryBarChart("productsCategoryChart");
    DashboardCharts.createSubCategoryChart("subCategoryChart");
    DashboardCharts.createMarginByCategoryChart("marginCategoryChart");

    const topTableColumns = [
      { key: "product" },
      { key: "sales", render: function (row) { return formatCurrency(row.sales); } },
      { key: "profit", render: function (row) { return formatCurrency(row.profit); } }
    ];

    renderTableBody("topProductsTable", dashboardData.topProducts, topTableColumns);
    renderTableBody("bottomProductsTable", dashboardData.bottomProducts, topTableColumns);

    const searchInput = document.getElementById("productSearchInput");
    if (searchInput) {
      searchInput.addEventListener("input", function () {
        const term = searchInput.value.trim().toLowerCase();
        const filteredTop = dashboardData.topProducts.filter(function (item) {
          return item.product.toLowerCase().includes(term);
        });
        const filteredBottom = dashboardData.bottomProducts.filter(function (item) {
          return item.product.toLowerCase().includes(term);
        });
        renderTableBody("topProductsTable", filteredTop, topTableColumns);
        renderTableBody("bottomProductsTable", filteredBottom, topTableColumns);
      });
    }
  }

  function renderTrendsPage() {
    DashboardCharts.createMonthlySalesChart("trendsMonthlyChart");
    DashboardCharts.createYearlyComparisonChart("yearlyComparisonChart");
    DashboardCharts.createQuarterlyChart("quarterlyBreakdownChart");
    DashboardCharts.createShippingAnalysisChart("trendsShippingChart");
    DashboardCharts.createCustomerTypeChart("trendsCustomerTypeChart");
  }

  function renderForecastPage() {
    DashboardCharts.createForecastChart("forecastChart");

    const metrics = dashboardData.forecastMetrics || {};
    const metricsMap = {
      r2: Number(metrics.r2 || 0).toFixed(4),
      rmse: formatCurrency(metrics.rmse || 0),
      slope: formatCurrency(metrics.slope || 0),
      intercept: formatCurrency(metrics.intercept || 0)
    };

    Object.keys(metricsMap).forEach(function (key) {
      const element = document.querySelector("[data-metric='" + key + "']");
      if (element) {
        element.textContent = metricsMap[key];
      }
    });

    const futureRows = dashboardData.forecastData.filter(function (item) {
      return item.actual === null;
    });

    renderTableBody("forecastTable", futureRows, [
      { key: "month" },
      { key: "predicted", render: function (row) { return formatCurrency(row.predicted); } },
      {
        key: "lower",
        render: function (row) {
          return formatCurrency(Number(row.predicted) * 0.85);
        }
      },
      {
        key: "upper",
        render: function (row) {
          return formatCurrency(Number(row.predicted) * 1.15);
        }
      }
    ]);

    const insights = [
      "The linear regression model captures the overall monthly direction with an R² of " + metricsMap.r2 + ".",
      "The next 6 months continue the current trend with expected sales centered around the predicted line.",
      "The confidence band is shown at ±15%, giving a planning range for inventory and target setting."
    ];

    const container = document.getElementById("forecastInsights");
    if (container) {
      container.innerHTML = insights.map(function (item) {
        return "<div class='insight-item'>" + item + "</div>";
      }).join("");
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    setActiveSidebarLink();
    setupSidebarToggle();
    setupIntersectionObserver();

    if (!window.dashboardData || !window.DashboardCharts) {
      return;
    }

    const page = getPage();
    if (page === "dashboard") {
      renderDashboardPage();
    } else if (page === "regional") {
      renderRegionalPage();
    } else if (page === "products") {
      renderProductsPage();
    } else if (page === "trends") {
      renderTrendsPage();
    } else if (page === "forecasting") {
      renderForecastPage();
    }

    makeTablesSortable();
  });
})();
