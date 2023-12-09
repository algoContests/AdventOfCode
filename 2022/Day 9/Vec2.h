
template<class T>
class Vec2
{
public:
    Vec2() : x(0), y(0) {}
    Vec2(T _x, T _y) : x(_x), y(_y) {}
    ~Vec2() {}

    inline Vec2& operator+=(const Vec2& v) { x += v.x; y += v.y; return *this; }
    inline Vec2& operator-=(const Vec2& v) { x -= v.x; y -= v.y; return *this; }
    inline Vec2& operator*=(const Vec2& v) { x *= v.x; y *= v.y; return *this; }
    inline Vec2& operator/=(const Vec2& v) { x /= v.x; y /= v.y; return *this; }
    inline Vec2& operator*=(T s) { x *= s; y *= s; return *this; }
    inline Vec2& operator/=(T s) { x /= s; y /= s; return *this; }

    inline Vec2 operator+(const Vec2& v) const { return Vec2(*this) += v; }
    inline Vec2 operator-(const Vec2& v) const { return Vec2(*this) -= v; }
    inline Vec2 operator*(const Vec2& v) const { return Vec2(*this) *= v; }
    inline Vec2 operator/(const Vec2& v) const { return Vec2(*this) /= v; }
    inline Vec2 operator*(T s) const { return Vec2(*this) *= s; }
    inline Vec2 operator/(T s) const { return Vec2(*this) /= s; }

    inline Vec2 operator-(void) const { return Vec2(-x, -y); }

    friend inline Vec2 operator*(T lhs, const Vec2& rhs) { return Vec2(rhs) *= lhs; }

    inline bool operator==(const Vec2& v) const { return x == v.x && y == v.y; }
    inline bool operator!=(const Vec2& v) const { return !(*this == v); }
    inline bool operator<(const Vec2& v) const { return this->y == v.y ? this->x < v.x : this->y < v.y; }
    inline bool operator>(const Vec2& v) const { return this->y == v.y ? this->x > v.x : this->y > v.y; }

    inline friend std::ostream& operator<<(std::ostream& os, const Vec2<T>& v) { os << v.x << " " << v.y; return os; };
    inline friend std::istream& operator>>(std::istream& is, Vec2<T>& v) { is >> v.x; is >> v.y; return is; };

public:
    T x;
    T y;
};

const map<Vec2<int>, Vec2<int>> TRAILING_MOVE
{
    { Vec2<int>(0, 0), Vec2<int>(0, 0) },

    { Vec2<int>(1, 0), Vec2<int>(0, 0) },
    { Vec2<int>(2, 0), Vec2<int>(1, 0) },
    { Vec2<int>(-1, 0), Vec2<int>(0, 0) },
    { Vec2<int>(-2, 0), Vec2<int>(-1, 0) },

    { Vec2<int>(0, 1), Vec2<int>(0, 0) },
    { Vec2<int>(0, 2), Vec2<int>(0, 1) },
    { Vec2<int>(0, -1), Vec2<int>(0, 0) },
    { Vec2<int>(0, -2), Vec2<int>(0, -1) },

    { Vec2<int>(1, 1), Vec2<int>(0, 0) },
    { Vec2<int>(-1, 1), Vec2<int>(0, 0) },
    { Vec2<int>(1, -1), Vec2<int>(0, 0) },
    { Vec2<int>(-1, -1), Vec2<int>(0, 0) },

    { Vec2<int>(2, 1), Vec2<int>(1, 1) },
    { Vec2<int>(-2, 1), Vec2<int>(-1, 1) },
    { Vec2<int>(2, -1), Vec2<int>(1, -1) },
    { Vec2<int>(-2, -1), Vec2<int>(-1, -1) },

    { Vec2<int>(1, 2), Vec2<int>(1, 1) },
    { Vec2<int>(-1, 2), Vec2<int>(-1, 1) },
    { Vec2<int>(1, -2), Vec2<int>(1, -1) },
    { Vec2<int>(-1, -2), Vec2<int>(-1, -1) },

    { Vec2<int>(2, 2), Vec2<int>(1, 1) },
    { Vec2<int>(-2, 2), Vec2<int>(-1, 1) },
    { Vec2<int>(2, -2), Vec2<int>(1, -1) },
    { Vec2<int>(-2, -2), Vec2<int>(-1, -1) }
}

struct sInfo {
    char dir;
    int dist;
};