# Forms, Events & UI Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

- [Form Types](#form-types)
- [Opening Forms](#opening-forms)
- [Form Data](#form-data)
- [Form Class Pattern](#form-class-pattern)
- [Form Events](#form-events)
- [Key Events Reference](#key-events-reference)
- [Common Form Objects](#common-form-objects)
- [List Box Patterns](#list-box-patterns)
- [Subforms](#subforms)
- [Object Methods](#object-methods)
- [TRACE in Compiled Code](#trace-in-compiled-code)
- [Go Deeper](#go-deeper)

---

## Form Types

| Type | Purpose | Typical Use |
|------|---------|-------------|
| **Input (detail) form** | Display/edit a single record or page of data | `MODIFY RECORD`, `ADD RECORD`, page subforms |
| **Output (list) form** | Display multiple records in a list/table layout | `DISPLAY SELECTION`, list subforms, report printing |
| **Dialog form** | Custom modal/modeless UI not tied to a record | `DIALOG` command, settings screens, wizards |

Forms can be **project forms** (standalone) or **table forms** (associated with a specific table).

---

## Opening Forms

### DIALOG command

The primary way to display a custom form. Full control over content, navigation, and validation.

```4d
// Basic modal dialog
$win:=Open form window("MyForm"; Movable form dialog box)
DIALOG("MyForm")
If (OK=1)  // User accepted
End if
CLOSE WINDOW($win)

// Dialog with formData -- Form.name and Form.age available inside
DIALOG("EditPerson"; New object("name"; "John"; "age"; 30))

// Non-modal (floating palette) using * parameter
$win:=Open form window("tools"; Palette form window)
DIALOG("tools"; *)  // Returns control immediately
```

Closing: **accept** (Enter, `ACCEPT`, `ak accept`) sets `OK=1`. **Cancel** (Escape, `CANCEL`, `ak cancel`) sets `OK=0`.

### Open form window

Always call **before** `DIALOG`. Window types: `Plain form window`, `Movable form dialog box`, `Palette form window`, `Modal dialog box`.

### ADD RECORD / MODIFY RECORD

Table-bound commands that display the current input form and handle record loading/saving automatically:

```4d
ADD RECORD([Customers])       // New record
MODIFY RECORD([Customers])    // Edit current record
```

---

## Form Data

The `Form` command returns the object associated with the current form.

```4d
var $data : Object
$data:=New object("version"; "12"; "items"; New collection)
DIALOG("MyForm"; $data)
```

Inside the form (form method or any object method):

```4d
$v:=Form.version        // "12"
Form.version:=13         // Update value -- reflected in caller's $data (by reference)
```

### Priority rules

1. If `formData` is passed to `DIALOG` -- `Form` returns that object (class is NOT instantiated).
2. If no `formData` but a **user class** is associated -- `Form` returns an instance of that class.
3. If neither -- `Form` returns a new empty object.

### Subform context

- Parent container typed as **object**: `Form` returns that object's value.
- Otherwise: `Form` returns an empty object maintained by 4D in the subform context.

---

## Form Class Pattern

Modern v21 approach: associate a **user class** with a form via the Form Editor's "Form Class" property. 4D auto-instantiates the class on load. Properties and functions are accessible via `Form`.

```4d
// Class: MyFormHandler
Class constructor()
    This.title:="My Dialog"
    This.items:=New collection

Function validate() : Boolean
    return (This.title#"")

Function loadData()
    This.items:=ds.Items.all().toCollection("name, price")
```

In the form method:

```4d
Case of
    :(Form event code=On Load)
        Form.loadData()
    :(Form event code=On Clicked)
        If (OBJECT Get name(Object current)="btnValidate")
            If (Form.validate())
                ACCEPT
            End if
        End if
End case
```

Usage -- no formData needed:

```4d
$win:=Open form window("ItemsDialog"; Movable form dialog box)
DIALOG("ItemsDialog")  // Form class is auto-instantiated
```

Note: passing `formData` to `DIALOG` **overrides** the form class (the class is not instantiated).

---

## Form Events

### Event handling pattern

```4d
Case of
    :(Form event code=On Load)
        // Initialize
    :(Form event code=On Clicked)
        // Handle click
    :(Form event code=On Data Change)
        // Value was modified
    :(Form event code=On Close Box)
        CANCEL
End case
```

### FORM Event (object version)

Returns an event object with additional properties (especially useful with list boxes):

```4d
var $event : Object
$event:=FORM Event
// $event.code, $event.description, $event.objectName
// For list boxes: $event.column, $event.columnName, $event.row
```

### Event flow

1. Object methods receive events first (column methods before list box method).
2. The form method receives events second.
3. Events must be **enabled** on both the object AND the form to fire.

---

## Key Events Reference

| Event | Code | When it fires |
|-------|------|---------------|
| **On Load** | 1 | Form about to display/print. All enabled objects called, then form method. |
| **On Clicked** | 4 | User clicked an object. Usually fires on mouse button release. |
| **On Double Clicked** | 13 | Double-click. `On Clicked` fires first, then `On Double Clicked`. |
| **On Timer** | 27 | Fires at intervals set by `SET TIMER`. |
| **On Before Keystroke** | 17 | Character about to be typed. Use `Keystroke` to read/filter. |
| **On After Keystroke** | 28 | Character was typed. Object value already updated. |
| **On Data Change** | 20 | Object value changed (after focus lost or value committed). |
| **On Validate** | 3 | Form data being accepted. Validate before `ACCEPT` completes. |
| **On Close Box** | 22 | Window close button clicked. Must call `CANCEL` or `ACCEPT` explicitly. |

### On Load details

- Fires for all objects on current page + page 0 with On Load enabled.
- Subform On Load fires **before** parent form's On Load.
- Must be enabled at **both** object and form level.

### On Clicked details

- Invisible buttons: fires immediately (no wait for mouse release).
- Combo boxes / drop-down lists: fires only when user selects a different value.
- Use `Clickcount` to detect number of clicks.

---

## Common Form Objects

### Input fields
Enterable or non-enterable areas for text, numbers, dates, times, or pictures. Support entry filters, placeholders, spell checking, multi-style text. Bound to fields or expressions.

### Buttons
Trigger actions on click. Variable = 0 by default, set to 1 on click. Supports standard actions and custom methods (method executes before the standard action). Styles: Regular, Flat, Toolbar, Bevel, Circle, Custom, etc.

### Checkboxes
Boolean controls: True/False. Three-state with integer: 0=unchecked, 1=checked, 2=semi-checked.

### Radio buttons
Mutually exclusive within a group. Selecting one deselects others in the same group.

### List boxes
Complex multi-column objects with four data source types:
- **Array** -- each column bound to a 4D array
- **Current selection / Named selection** -- columns bound to fields/expressions
- **Collection / Entity selection** -- columns use `This.<property>` expressions

### Combo boxes
Editable text input + drop-down suggestions. Handle via `On Before Keystroke`, `On After Keystroke`, `On Data Change`.

### Dropdown lists
Non-editable pick list. `On Clicked` fires only on value change.

### Subforms
Forms embedded in other forms. **List subforms** show related records; **page subforms** embed a form page for widgets and complex UI.

---

## List Box Patterns

### Entity selection source

The most common modern pattern:

```4d
// On Load
Form.employees:=ds.Employee.all()
Form.employees:=ds.Employee.query("department = :1"; "Sales")
```

Column expressions: `This.lastName`, `This.firstName`, `This.department.name`.

Selection properties (set in list box properties):
- **Current item** -- object receiving the selected entity
- **Current item position** -- longint with selected row index
- **Selected items** -- entity selection of all selected rows

### Collection source

```4d
Form.items:=New collection
Form.items.push(New object("name"; "Item A"; "price"; 10))
```

Column expressions: `This.name`, `This.price`. Same selection properties as entity selection.

To refresh after programmatic changes, **reassign** the collection:

```4d
Form.items:=Form.items.push("new value")  // Reassign triggers refresh
```

### Handling selection

```4d
Case of
    :(Form event code=On Selection Change)
        // Form.currentItem has the selected entity/object
    :(Form event code=On Double Clicked)
        $event:=FORM Event  // $event.row, $event.column
End case
```

### Sorting

Standard sort works by clicking headers. For custom sorts:

```4d
If (Form event code=On Header Click)
    Form.employees:=Form.employees.orderBy("lastName asc")
End if
```

---

## Subforms

### Two types

| Type | Purpose |
|------|---------|
| **List subform** | Displays records from a related Many table. |
| **Page subform** | Embeds a form page. Used for widgets, complex UI. |

### Container-subform communication

**Parent to subform** (single value):

```4d
// In the SUBFORM form method:
If (Form event code=On Bound Variable Change)
    Form.clockValue:=OBJECT Get subform container value
End if
```

**Subform to parent** (single value):

```4d
// In the SUBFORM:
OBJECT SET SUBFORM CONTAINER VALUE(newValue)
// Triggers On Data Change on the subform container in the parent
```

**Object-based sharing** (preferred for multiple values): type the subform container variable as **object**. Both parent and subform share the same object via `Form`.

---

## Object Methods

### OBJECT SET / OBJECT GET

Control object properties at runtime. The `*` first parameter means "find by name in the current form".

```4d
OBJECT SET VISIBLE(*; "myButton"; False)
OBJECT SET ENABLED(*; "myInput"; True)
OBJECT SET FONT(*; "myField"; "Helvetica")
OBJECT SET FONT SIZE(*; "myField"; 14)
OBJECT SET RGB COLORS(*; "myField"; 0x0000FF; 0xFFFFFF)
OBJECT SET SCROLL POSITION(*; "myListbox"; $row; *)
```

### Getting object info

```4d
$name:=OBJECT Get name(Object current)
$ptr:=OBJECT Get pointer(Object current)
$ptr:=OBJECT Get pointer(Object subform container)
```

---

## TRACE in Compiled Code

**Compiled 4D code ignores `TRACE` entirely.** Safe to leave in code -- does nothing when compiled. Worth noting in reviews but **never a blocker**.

---

## Go Deeper

- **Events index** -- full list of all form events: `references/events-index.md`
- **Form objects index** -- all form object types: `references/form-objects-index.md`
- **Manual insights** -- real-world gotchas: `references/manual-insights.md`
- **Key doc files:**
  - `docs/FormEditor/formEditor.md` -- Form Editor UI
  - `docs/FormObjects/listbox_overview.md` -- Full list box docs
  - `docs/FormObjects/subform_overview.md` -- Subform details
  - `docs/commands/dialog.md` -- DIALOG command
  - `docs/commands/form.md` -- Form command
  - `docs/Events/onLoad.md`, `docs/Events/onClicked.md` -- Event details
