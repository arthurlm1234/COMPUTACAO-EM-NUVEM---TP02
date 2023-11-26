wget --server-response \
     --output-document response.out \
     --header='Content-Type: application/json' \
     --post-data '{"songs": ["Yesterday", "Bohemian Rhapsody", "Hey Ya!"]}' \
     http://10.110.77.0:32171/api/recommend