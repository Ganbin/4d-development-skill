# 4D Form Development

4D form development, design, and implementation including JSON forms, events, and objects.

## Form Types

- **Project Forms**: Independent forms not attached to tables
- **Table Forms**: Attached to specific tables (DEPRECATED for new development)

## Form Structure & Pages

- **Page 0 (Background)**: Contents displayed on all pages, ideal for navigation
- **Page 1+**: Main display pages for content and data entry

## JSON Form Definition

```json
{
    "windowTitle": "Form Title",
    "windowMinWidth": 400,
    "windowMinHeight": 300,
    "method": "formMethod",
    "pages": [
        null,  // Page 0 (background)
        {
            "objects": {
                "textField": {
                    "type": "input",
                    "dataSource": "fieldName",
                    "left": 20,
                    "top": 20,
                    "width": 200,
                    "height": 20
                },
                "button": {
                    "type": "button",
                    "text": "OK",
                    "action": "accept",
                    "left": 20,
                    "top": 60,
                    "width": 80,
                    "height": 24
                }
            }
        }
    ]
}
```

## Form Objects

### Input Objects
- Text Input, Dropdown Lists, Checkboxes, Radio Buttons

### Display Objects
- Static Text, Static Pictures, Shapes

### Interactive Objects
- Buttons, Picture Buttons, Tab Controls

### Advanced Objects
- List Boxes, Subforms, Group Boxes

## Form Events

### Form-Level Events
- `On Load`: Form initialization
- `On Unload`: Form cleanup
- `On Close Box`: Window close handling
- `On Resize`: Window size changes

### Object-Level Events
- `On Clicked`: Button and interactive object clicks
- `On Data Change`: Field value modifications
- `On Getting Focus`/`On Losing Focus`: Field navigation
- `On Selection Change`: List and selection object changes

## Best Practices

1. **Use JSON form definitions** for modern forms
2. **Page 0 for navigation** - Consistent button placement
3. **Logical field grouping** - Organize by topic/page
4. **Clear entry order** - Tab order for efficient data entry
5. **Responsive design** - Handle window sizing
6. **Form methods for logic** - Centralize form behavior
7. **Object methods for interaction** - Specific object handling

## Reference

Complete JSON schema available at: `context/formsSchema-4d-v20-r9.json` (bundled with this skill)

For detailed form development, see official docs: https://developer.4d.com/docs/FormEditor/
