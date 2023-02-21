# build the services
docker image build -t exchange exchange
docker image build -t market-data-provider market-data-provider

# start the stack
docker compose up