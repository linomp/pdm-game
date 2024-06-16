# RUL Experiments

## 16.06.2024

Still with sklearn, Support Vector Regression.

### Model trained with maintenace, tested on run-to-failure dataset

![immagine](./img/16_06_2024_trained_with_maintenance_test_run_to_failure.png)
![immagine](./img/rul_with_maintenance_test_with_run_to_failure.png)

### Model trained with run-to-failure, tested on dataset with maintenance

![immagine](./img/16_06_2024_trained_run_to_failure_test_with_maintenance.png)
![immagine](./img/rul_run_to_failure_test_with_maintenance.png)

## 15.06.2024

With sklearn, Support Vector Regression model:

### Run-to-failure

Training R^2: `0.9987058235956183`

Testing R^2: `0.9993135719482489`

![immagine](./img/15_06_2024_without_maintenance.png)

### Simulating maintenance

Training R^2: `0.8436921735713233`

Testing R^2: `0.7575825125374217`

![immagine](./img/15_06_2024_with_maintenance.png)

## 26.05.2024

With darts library, ExponentialSmoothing model:

### Run-to-failure

![img.png](./img/26_05_2024_health_forecast.png)
