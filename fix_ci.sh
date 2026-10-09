sed -i 's/uses: SonarSource\/sonarqube-quality-gate-action@v1.3.0/uses: sonarsource\/sonarqube-quality-gate-action@v1.2.1/i' .github/workflows/sonarqube.yml
sed -i 's/runs-on: ubuntu-latest/runs-on: ubuntu-24.04/g' .github/workflows/*.yml
