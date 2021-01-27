source ../.envrc

for i in {1..100000}; do
  eval $1
  sleep 5
done
