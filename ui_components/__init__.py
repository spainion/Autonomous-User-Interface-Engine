"""
UI Components Library
Pre-built, customizable UI components
"""

# Button components
BUTTON_COMPONENTS = {
    'primary': '''
<button class="btn btn-primary px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
    Primary Button
</button>
''',
    'secondary': '''
<button class="btn btn-secondary px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors">
    Secondary Button
</button>
''',
    'outline': '''
<button class="btn btn-outline px-4 py-2 border-2 border-blue-600 text-blue-600 rounded-lg hover:bg-blue-600 hover:text-white transition-all">
    Outline Button
</button>
'''
}

# Form components
FORM_COMPONENTS = {
    'input_text': '''
<div class="form-group mb-4">
    <label for="input" class="block text-sm font-medium text-gray-700 mb-2">Label</label>
    <input type="text" id="input" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Enter text">
</div>
''',
    'textarea': '''
<div class="form-group mb-4">
    <label for="textarea" class="block text-sm font-medium text-gray-700 mb-2">Message</label>
    <textarea id="textarea" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Your message"></textarea>
</div>
''',
    'select': '''
<div class="form-group mb-4">
    <label for="select" class="block text-sm font-medium text-gray-700 mb-2">Select Option</label>
    <select id="select" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option>Option 1</option>
        <option>Option 2</option>
        <option>Option 3</option>
    </select>
</div>
'''
}

# Navigation components
NAV_COMPONENTS = {
    'navbar': '''
<nav class="bg-white shadow-lg">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center py-4">
            <div class="text-2xl font-bold text-gray-800">Logo</div>
            <div class="hidden md:flex space-x-6">
                <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors">Home</a>
                <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors">About</a>
                <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors">Services</a>
                <a href="#" class="text-gray-600 hover:text-blue-600 transition-colors">Contact</a>
            </div>
            <button class="md:hidden text-gray-600">☰</button>
        </div>
    </div>
</nav>
''',
    'sidebar': '''
<aside class="w-64 bg-gray-800 text-white min-h-screen p-4">
    <div class="mb-8">
        <h2 class="text-2xl font-bold">Dashboard</h2>
    </div>
    <nav class="space-y-2">
        <a href="#" class="block px-4 py-2 rounded hover:bg-gray-700 transition-colors">Home</a>
        <a href="#" class="block px-4 py-2 rounded hover:bg-gray-700 transition-colors">Analytics</a>
        <a href="#" class="block px-4 py-2 rounded hover:bg-gray-700 transition-colors">Settings</a>
        <a href="#" class="block px-4 py-2 rounded hover:bg-gray-700 transition-colors">Profile</a>
    </nav>
</aside>
'''
}

# Card components
CARD_COMPONENTS = {
    'basic': '''
<div class="bg-white rounded-lg shadow-md overflow-hidden max-w-sm">
    <img src="placeholder.jpg" alt="Card image" class="w-full h-48 object-cover">
    <div class="p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-2">Card Title</h3>
        <p class="text-gray-600 mb-4">Card description goes here with some details about the content.</p>
        <button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors">Learn More</button>
    </div>
</div>
''',
    'profile': '''
<div class="bg-white rounded-lg shadow-md p-6 max-w-sm text-center">
    <img src="profile.jpg" alt="Profile" class="w-24 h-24 rounded-full mx-auto mb-4">
    <h3 class="text-xl font-bold text-gray-800 mb-1">John Doe</h3>
    <p class="text-gray-600 mb-4">Software Engineer</p>
    <div class="flex justify-center space-x-4">
        <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Connect</button>
        <button class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50">Message</button>
    </div>
</div>
'''
}

# Modal components
MODAL_COMPONENTS = {
    'basic': '''
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg max-w-md w-full p-6">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Modal Title</h2>
        <p class="text-gray-600 mb-6">Modal content goes here.</p>
        <div class="flex justify-end space-x-3">
            <button class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50">Cancel</button>
            <button class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Confirm</button>
        </div>
    </div>
</div>
'''
}

# Alert components
ALERT_COMPONENTS = {
    'success': '''
<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative" role="alert">
    <strong class="font-bold">Success!</strong>
    <span class="block sm:inline">Your action was completed successfully.</span>
</div>
''',
    'error': '''
<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
    <strong class="font-bold">Error!</strong>
    <span class="block sm:inline">Something went wrong.</span>
</div>
'''
}

# Table components
TABLE_COMPONENTS = {
    'basic': '''
<div class="overflow-x-auto">
    <table class="min-w-full bg-white border border-gray-300">
        <thead class="bg-gray-100">
            <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
            <tr class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">John Doe</td>
                <td class="px-6 py-4 whitespace-nowrap">john@example.com</td>
                <td class="px-6 py-4 whitespace-nowrap">Admin</td>
            </tr>
        </tbody>
    </table>
</div>
'''
}

ALL_COMPONENTS = {
    'buttons': BUTTON_COMPONENTS,
    'forms': FORM_COMPONENTS,
    'navigation': NAV_COMPONENTS,
    'cards': CARD_COMPONENTS,
    'modals': MODAL_COMPONENTS,
    'alerts': ALERT_COMPONENTS,
    'tables': TABLE_COMPONENTS
}
