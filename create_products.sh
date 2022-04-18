http 127.0.0.1:5000/products/add_batch quantity=10 reference=bath1 sku=table
http 127.0.0.1:5000/products/add_batch quantity=140 reference=chairbatch sku=chair
http 127.0.0.1:5000/products/add_batch quantity=40 reference=bath333 sku=chair
http 127.0.0.1:5000/products/allocate sku=chair quantity=10 orderid=commandedeux 
http 127.0.0.1:5000/products/allocate sku=table quantity=4 orderid=commandeune 
http 127.0.0.1:5000/products/allocate sku=chair quantity=100 orderid=grossecommande
