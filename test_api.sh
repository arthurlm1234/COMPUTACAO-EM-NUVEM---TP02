wget --server-response \
     --output-document response.out \
     --header='Content-Type: application/json' \
     --post-data '{"songs": ["Yesterday", "Bohemian Rhapsody"]}' \
     http://10.244.0.140:32171/api/recommend