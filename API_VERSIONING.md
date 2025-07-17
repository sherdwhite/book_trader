# API Versioning Implementation

This document explains the API versioning structure implemented for the BookTrader API.

## Structure

```
api/
├── __init__.py
├── apps.py
├── urls.py              # Main API routing with versioning
├── v1/                  # Version 1 API
│   ├── __init__.py
│   ├── urls.py         # V1 specific routes
│   ├── views.py        # V1 viewsets
│   └── serializers.py  # V1 serializers
└── tests/              # API tests

# Future structure (when implementing v2):
# ├── v2/                  # Version 2 API
# │   ├── __init__.py
# │   ├── urls.py         # V2 specific routes
# │   └── views.py        # V2 viewsets (with enhanced features)
```

## URL Patterns

With this implementation, your API now supports:

1. **Versioned endpoints:**
   - `/api/v1/books/` - Version 1 books endpoint
   - `/api/v1/authors/` - Version 1 authors endpoint
   - `/api/v1/publishers/` - Version 1 publishers endpoint
   - `/api/v1/ratings/` - Version 1 ratings endpoint
   - `/api/v1/users/` - Version 1 users endpoint

2. **Backward compatibility:**
   - `/api/books/` - Still works (routes to v1)
   - `/api/authors/` - Still works (routes to v1)
   - etc.

3. **Future versions (when implemented):**
   - `/api/v2/books/` - Ready when you implement v2

## Benefits

1. **Backward Compatibility**: Existing clients continue to work
2. **Gradual Migration**: Clients can migrate to new versions at their own pace
3. **Feature Evolution**: New versions can have enhanced features without breaking old clients
4. **Clear API Contract**: Version numbers make it clear what features are available

## Adding a New Version

To add a new API version (e.g., v2):

1. Create a new directory: `api/v2/`
2. Copy the structure from `v1/` as a starting point
3. Modify the views/serializers for new features
4. Add the URL pattern in `api/urls.py`:
   ```python
   path('v2/', include('api.v2.urls')),
   ```

## Migration Strategy

When you're ready to add new features:

1. Keep v1 unchanged for existing clients
2. Implement new features in v2
3. Document the differences between versions
4. Provide migration guides for clients
5. Eventually deprecate older versions with proper notice

## Current Status

- ✅ V1 API is active and maintains all current functionality
- ✅ Backward compatibility is preserved
- ✅ URL routing supports multiple versions
- 📋 V2 structure is planned for future implementation

Your existing functionality remains unchanged, but you now have a solid foundation for API evolution.
