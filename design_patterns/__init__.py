"""
Design Patterns Library
Templates for common design patterns and page layouts
"""

LANDING_PAGE_PATTERN = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Hero Section -->
    <section class="hero bg-primary text-white py-5">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6">
                    <h1 class="display-4 fw-bold mb-3">Transform Your Business</h1>
                    <p class="lead mb-4">Powerful solutions for modern companies</p>
                    <button class="btn btn-light btn-lg">Get Started</button>
                </div>
                <div class="col-lg-6">
                    <img src="hero-image.jpg" alt="Hero" class="img-fluid">
                </div>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features py-5">
        <div class="container">
            <h2 class="text-center mb-5">Features</h2>
            <div class="row">
                <div class="col-md-4 text-center">
                    <div class="mb-3">🚀</div>
                    <h4>Fast</h4>
                    <p>Lightning-fast performance</p>
                </div>
                <div class="col-md-4 text-center">
                    <div class="mb-3">🔒</div>
                    <h4>Secure</h4>
                    <p>Enterprise-grade security</p>
                </div>
                <div class="col-md-4 text-center">
                    <div class="mb-3">⚡</div>
                    <h4>Reliable</h4>
                    <p>99.9% uptime guarantee</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta bg-light py-5">
        <div class="container text-center">
            <h2 class="mb-4">Ready to Get Started?</h2>
            <button class="btn btn-primary btn-lg">Sign Up Now</button>
        </div>
    </section>
</body>
</html>
'''

DASHBOARD_PATTERN = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="d-flex">
        <!-- Sidebar -->
        <nav class="bg-dark text-white p-3" style="width: 250px; min-height: 100vh;">
            <h4 class="mb-4">Dashboard</h4>
            <ul class="nav flex-column">
                <li class="nav-item"><a href="#" class="nav-link text-white">Home</a></li>
                <li class="nav-item"><a href="#" class="nav-link text-white">Analytics</a></li>
                <li class="nav-item"><a href="#" class="nav-link text-white">Reports</a></li>
                <li class="nav-item"><a href="#" class="nav-link text-white">Settings</a></li>
            </ul>
        </nav>
        
        <!-- Main Content -->
        <div class="flex-grow-1">
            <!-- Top Bar -->
            <nav class="navbar navbar-light bg-light border-bottom">
                <div class="container-fluid">
                    <span class="navbar-brand">Analytics Dashboard</span>
                    <div>
                        <span class="me-3">User Name</span>
                        <img src="avatar.jpg" alt="Avatar" class="rounded-circle" width="40">
                    </div>
                </div>
            </nav>
            
            <!-- Dashboard Content -->
            <div class="p-4">
                <!-- Stats Cards -->
                <div class="row mb-4">
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h6 class="text-muted">Total Users</h6>
                                <h3>1,234</h3>
                                <small class="text-success">+12% from last month</small>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card">
                            <div class="card-body">
                                <h6 class="text-muted">Revenue</h6>
                                <h3>$12,345</h3>
                                <small class="text-success">+8% from last month</small>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Chart Area -->
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Analytics Overview</h5>
                        <canvas id="chart" height="300"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

ECOMMERCE_PRODUCT_PATTERN = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container py-5">
        <div class="row">
            <!-- Product Images -->
            <div class="col-md-6">
                <img src="product.jpg" alt="Product" class="img-fluid rounded mb-3">
                <div class="d-flex gap-2">
                    <img src="thumb1.jpg" class="img-thumbnail" width="80">
                    <img src="thumb2.jpg" class="img-thumbnail" width="80">
                    <img src="thumb3.jpg" class="img-thumbnail" width="80">
                </div>
            </div>
            
            <!-- Product Details -->
            <div class="col-md-6">
                <h1 class="mb-3">Product Name</h1>
                <div class="mb-3">
                    <span class="text-warning">★★★★☆</span>
                    <span class="text-muted ms-2">(123 reviews)</span>
                </div>
                <h2 class="text-primary mb-4">$99.99</h2>
                
                <p class="mb-4">Product description goes here with all the important details and features.</p>
                
                <div class="mb-4">
                    <label class="form-label">Size:</label>
                    <select class="form-select">
                        <option>Small</option>
                        <option>Medium</option>
                        <option>Large</option>
                    </select>
                </div>
                
                <div class="mb-4">
                    <label class="form-label">Quantity:</label>
                    <input type="number" class="form-control" value="1" min="1">
                </div>
                
                <button class="btn btn-primary btn-lg w-100 mb-3">Add to Cart</button>
                <button class="btn btn-outline-secondary btn-lg w-100">Add to Wishlist</button>
            </div>
        </div>
        
        <!-- Product Details Tabs -->
        <div class="row mt-5">
            <div class="col-12">
                <ul class="nav nav-tabs">
                    <li class="nav-item">
                        <a class="nav-link active" href="#description">Description</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#reviews">Reviews</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#shipping">Shipping</a>
                    </li>
                </ul>
                <div class="border p-4">
                    <p>Detailed product information goes here...</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

ALL_PATTERNS = {
    'landing_page': LANDING_PAGE_PATTERN,
    'dashboard': DASHBOARD_PATTERN,
    'ecommerce_product': ECOMMERCE_PRODUCT_PATTERN
}
