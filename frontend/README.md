# UPI Fraud Detection System - Frontend

Beautiful Next.js frontend with TailwindCSS for UPI fraud detection system.

## Features

- 🎨 Modern, responsive UI with TailwindCSS
- 🔐 Secure authentication with JWT
- 📊 Interactive dashboard with real-time analytics
- 📈 Transaction visualization with charts
- ⚡ Real-time fraud detection alerts
- 🎯 Beautiful gradient designs and animations

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: TailwindCSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast
- **Language**: TypeScript

## Setup Instructions

1. **Install dependencies**:

```bash
cd frontend
npm install
```

2. **Configure environment variables**:

```bash
# Create .env.local file (already created)
# Update NEXT_PUBLIC_API_URL if your backend runs on different port
```

3. **Run development server**:

```bash
npm run dev
```

4. **Open browser**:

```
http://localhost:3000
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with auth provider
│   ├── page.tsx            # Landing page
│   ├── login/
│   │   └── page.tsx        # Login page
│   ├── register/
│   │   └── page.tsx        # Registration page
│   └── dashboard/
│       └── page.tsx        # Main dashboard
├── context/
│   └── AuthContext.tsx     # Authentication context
├── lib/
│   ├── api.ts              # Axios instance with interceptors
│   ├── auth.ts             # Auth service functions
│   └── transactions.ts     # Transaction service functions
├── public/                 # Static assets
└── tailwind.config.js      # TailwindCSS configuration
```

## Features Overview

### Landing Page

- Beautiful hero section with gradients
- Feature showcase
- Statistics display
- Call-to-action buttons

### Authentication

- Login with username/password
- Registration with profile details
- JWT token management
- Automatic token refresh

### Dashboard

- Real-time statistics cards
- Fraud trend visualization
- Recent transactions table
- Quick action buttons
- Transaction creation modal
- Fraud alerts banner

### Design Highlights

- Gradient backgrounds and buttons
- Smooth animations and transitions
- Responsive design for all screen sizes
- Custom color palette for fraud detection
- Interactive charts and graphs
- Modern card-based layout

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT
