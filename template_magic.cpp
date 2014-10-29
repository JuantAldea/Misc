template <typename THead, typename ...TTail>
class MagicContainer : public MagicContainer <TTail ...>
{
    public:
        THead data;

        MagicContainer(){}

        THead getData(THead) const
        {
            return data;
        }

        void setData(const THead &o)
        {
            data = o;
        }
}

template <>
class MagicContainer
{
    MagicContainer(){}
    void setData(){}
    void getData(){}
}

#include <iostream>
using namespace std;

int main(void)
{
    MagicContainer<int, double, float, char> container;
    container.setData((int) 1);
    cout << container.getData(int) << endl;
    return 0;
}
