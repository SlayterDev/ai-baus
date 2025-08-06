# Frontend Components

This directory contains all the React components for the AI Boss application, organized in a modular structure.

## Component Structure

```
components/
├── index.js                 # Main component exports
├── Header.js               # Application header with navigation
├── employees/              # Employee-related components
│   ├── index.js           # Employee component exports
│   ├── EmployeeManager.js # Employee management container
│   ├── EmployeeForm.js    # Employee creation form
│   └── EmployeeCard.js    # Individual employee display card
└── meetings/              # Meeting-related components
    ├── index.js           # Meeting component exports
    ├── MeetingManager.js  # Meeting management container
    ├── MeetingForm.js     # Meeting creation form
    ├── MeetingCard.js     # Individual meeting display card
    └── MeetingRoom.js     # Meeting chat interface
```

## Component Hierarchy

### Main App Structure
- `App.js` - Main application container
  - `Header` - Navigation and branding
  - `EmployeeManager` - Employee management section
  - `MeetingManager` - Meeting management section

### Employee Components
- `EmployeeManager` - Container for employee management
  - `EmployeeForm` - Modal form for creating employees
  - `EmployeeCard` - Individual employee display

### Meeting Components
- `MeetingManager` - Container for meeting management
  - `MeetingForm` - Modal form for creating meetings
  - `MeetingCard` - Individual meeting display
  - `MeetingRoom` - Active meeting chat interface

## Usage

### Importing Components
```javascript
// Import individual components
import { Header, EmployeeManager, MeetingManager } from './components';

// Import employee components specifically
import { EmployeeForm, EmployeeCard } from './components/employees';

// Import meeting components specifically
import { MeetingForm, MeetingCard, MeetingRoom } from './components/meetings';
```

### Component Props

#### EmployeeManager
- `employees` - Array of employee objects
- `onEmployeeChange` - Callback function when employees are modified

#### EmployeeForm
- `onClose` - Callback to close the form
- `onSuccess` - Callback when employee is created successfully

#### EmployeeCard
- `employee` - Employee object
- `onDelete` - Callback when employee is deleted

#### MeetingManager
- `meetings` - Array of meeting objects
- `employees` - Array of employee objects
- `onMeetingsChange` - Callback function when meetings are modified

#### MeetingForm
- `employees` - Array of employee objects
- `onClose` - Callback to close the form
- `onSuccess` - Callback when meeting is created successfully

#### MeetingCard
- `meeting` - Meeting object
- `employees` - Array of employee objects
- `onJoin` - Callback when meeting is joined

#### MeetingRoom
- `meeting` - Active meeting object
- `employees` - Array of employee objects
- `onExit` - Callback when exiting the meeting

## Backward Compatibility

The original `Meetings.js` file has been preserved as a re-export for backward compatibility. New code should use the modular components directly.

## Benefits of This Structure

1. **Modularity** - Each component has a single responsibility
2. **Reusability** - Components can be easily reused across the application
3. **Maintainability** - Easier to locate and modify specific functionality
4. **Testability** - Individual components can be tested in isolation
5. **Scalability** - Easy to add new components or modify existing ones
6. **Consistency** - Both employees and meetings follow the same organizational pattern 